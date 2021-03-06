odoo.define("kanban_draggable.kanban_renderer", function(require) {
"use strict";

var KanbanRenderer = require("web.KanbanRenderer");

KanbanRenderer.include({

    _setState: function (state) {
        this._super.apply(this, arguments);
        
        var arch = this.arch;
        this.columnOptions.sortable = true;
        if (arch.attrs.disable_sort_column) {
            if (arch.attrs.disable_sort_column == "true") {
                this.columnOptions.sortable = false;
            }
        }
    },
    
    _renderGrouped: function () {
        this._super.apply(this, arguments);
        
        if (this.columnOptions.sortable == false) {
            try {
                this.$el.sortable("disable");
            }
            catch (err) {}
        }
    }
    
});

});