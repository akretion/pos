odoo.define('pos_no_preload_product_image.chrome', function (require) {
    'use strict';

    const Chrome = require('point_of_sale.Chrome');
    const Registries = require('point_of_sale.Registries');

    const PosNoPreloadProductImageChrome = (Chrome) =>
        class extends Chrome {
           _preloadImages () {
                //do nothing !
            }
        };

    Registries.Component.extend(Chrome, PosNoPreloadProductImageChrome);

    return Chrome;
});
