odoo.define('point_of_sale.ProductItemNoImage', function(require) {
    'use strict';
    const ProductItem = require('point_of_sale.ProductItem');
    const Registries = require('point_of_sale.Registries');

    class ProductItemNoImage extends ProductItem {}
    ProductItemNoImage.template = 'ProductItemNoImage';

    Registries.Component.add(ProductItemNoImage);

    return ProductItem;
});
