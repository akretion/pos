odoo.define('ProductItem', function(require) {
    'use strict';
    const ProductItem = require('point_of_sale.ProductItem');
    const Registries = require('point_of_sale.Registries');

    ProductItem.include({
        get imageUrl() {
            const product = this.props.product;
            if(product.hasImage){
                return this._super();
            }
//            const product = this.props.product;
//            return `/web/image?model=product.product&field=image_128&id=${product.id}&write_date=${product.write_date}&unique=1`;
        }
    })
//    class ProductItemNoImage extends ProductItem {}
//    ProductItemNoImage.template = 'ProductItemNoImage';

//    Registries.Component.add(ProductItem);

    return ProductItem;
});
