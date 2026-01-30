/** @odoo-module */
import { PaymentInterface } from "@point_of_sale/app/payment/payment_interface";
import { register_payment_method } from "@point_of_sale/app/store/pos_store";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class PaymentCaisseAP extends PaymentInterface {
    setup() {
        super.setup(...arguments);

        // --- DEBUG LOGGING ---
        console.group("CaisseAP Debugger");

        const pm = this.payment_method_id;
        console.log("1. Payment Method:", pm.name);
        console.log("2. Configured Device ID:", pm.iot_device_id);

        // Check if the model exists in POS
        if (!this.pos.models["iot.device"]) {
            console.error("CRITICAL: 'iot.device' model is NOT loaded in POS.");
        } else {
            const allDevices = this.pos.models["iot.device"].getAll();
            console.log("3. Loaded Devices in Browser:", allDevices);

            // ID Lookup Logic
            let targetId = pm.iot_device_id;
            if (Array.isArray(targetId)) targetId = targetId[0]; // Handle [1, "Name"] format

            this.device = this.pos.models["iot.device"].get(targetId);
            console.log("4. Resolved Device Object:", this.device);
        }
        console.groupEnd();
        // ---------------------
    }

    // ... keep your send_payment_request and other methods ...
    async send_payment_request(cid) {
        // ... (keep code) ...
        // if (!this.device) {
        //      this._showError(_t("Config Error"), _t("Check Console logs (F12) for CaisseAP Debugger"));
        //      return false;
        // }

        const ip = 'localhost'; // this.device.ip;
        const port = 8888; // this.device.tcp_port || 8888;

        console.log(`[CaisseAP] Sending to ${ip}:${port}`);

        try {
            if (typeof TCPSocket === 'undefined') {
                throw new Error(
                    _t("Direct Sockets API is missing.\n\n" +
                       "1. Open chrome://flags\n" +
                       "2. Enable #enable-direct-sockets\n" +
                       "3. Or launch Chrome with flags: --enable-features=DirectSockets --restricted-api-origins=\"http://localhost:8069\"")
                );
            }

            const line = this.pos.get_order().get_paymentline(cid);
            const amount = line.get_amount();
            const currencyCode = this.pos.currency.name;

            const packet = this._buildPacket(amount, currencyCode, false);

            // Send TCP
            const response = await this._sendRawTcp(ip, port, packet);
            console.log("[CaisseAP] Raw Response:", response);

            // Parse
            const result = this._parseResponse(response);

            if (result.status === 'success') {
                line.set_payment_status('done');
                line.transaction_id = result.data.AC || '';
                return true;
            } else {
                this._showError(
                    _t("Payment Refused"),
                    `Terminal Status: AE=${result.data.AE} / AF=${result.data.AF || 'None'}`
                );
                line.set_payment_status('retry');
                return false;
            }

        } catch (error) {
            console.error("[CaisseAP] Exception:", error);
            this._showError(_t("Connection Error"), error.message || "Unknown error");

            const line = this.pos.get_order().get_paymentline(cid);
            if (line) line.set_payment_status('retry');
            return false;
        }
    }

    async send_payment_cancel(order, cid) {
        super.send_payment_cancel(order, cid);
        return true;
    }

    // ----------------------------------------------------------------------
    // Low Level TCP
    // ----------------------------------------------------------------------

    async _sendRawTcp(ip, port, dataString) {
        let socket = null;
        try {
            socket = new TCPSocket(ip, port);
            await socket.opened;

            const writer = socket.writable.getWriter();
            const encoder = new TextEncoder();
            await writer.write(encoder.encode(dataString));
            writer.releaseLock();

            const reader = socket.readable.getReader();
            const { value, done } = await reader.read();
            reader.releaseLock();

            await socket.close();

            if (value) {
                return new TextDecoder().decode(value);
            } else {
                throw new Error("Terminal accepted connection but returned no data.");
            }
        } catch (err) {
            if (socket) socket.close().catch(() => {});
            // Improve error message for common TCP issues
            if (err.name === 'NetworkError') {
                throw new Error(`Connection refused to ${ip}:${port}. Is the terminal/simulator running?`);
            }
            throw err;
        }
    }

    // ----------------------------------------------------------------------
    // Protocol
    // ----------------------------------------------------------------------

    _buildPacket(amount, currencyCode, isCheck) {
        const currencyMap = { 'EUR': '978', 'USD': '840' };
        const curNum = currencyMap[currencyCode] || '978';
        const amountCents = Math.round(amount * 100);
        const amountStr = amountCents.toString().padStart(2, '0');

        const tags = {
            'CZ': '0300', 'CJ': '012345678901', 'CA': '01',
            'CE': curNum, 'BA': '0', 'CD': '0', 'CB': amountStr
        };
        if (isCheck) tags['CC'] = '00C';

        let packet = "";
        if (tags.CZ) {
            packet += `CZ${this._len(tags.CZ)}${tags.CZ}`;
            delete tags.CZ;
        }
        for (const [key, val] of Object.entries(tags)) {
            packet += `${key}${this._len(val)}${val}`;
        }
        return packet;
    }

    _len(val) {
        return val.length.toString().padStart(3, '0');
    }

    _parseResponse(raw) {
        const data = {};
        let i = 0;
        while (i < raw.length) {
            if (i + 5 > raw.length) break;
            const tag = raw.substring(i, i + 2);
            const len = parseInt(raw.substring(i + 2, i + 5), 10);
            i += 5;
            if (isNaN(len)) break;
            const val = raw.substring(i, i + len);
            data[tag] = val;
            i += len;
        }
        return {
            status: data.AE === '10' ? 'success' : 'failure',
            data
        };
    }

    // ... keep other methods ...
    _showError(title, body) {
        this.pos.env.services.dialog.add(AlertDialog, { title, body });
    }
}

register_payment_method("caisse_ap", PaymentCaisseAP);
