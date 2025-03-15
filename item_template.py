from string import Template

item_templates = {}
item_templates["default"] = Template("""
switch(FEAT_STATIONS, SELF, sw_item_${name}_prepare, [
    ${temps}
]){return;}
item(FEAT_STATIONS, i_${name}){
    property {
        class: "${class_label}";
        classname: string(STR_CLASS_${class_label});
        name: string(STR_STAT_${name_label});
        tile_flags: [""" + ",\n".join("bitmask(STAT_TILE_PYLON)" for i in range(8)) +
"""            ];
    } graphics {
        prepare_layout: sw_item_${name}_prepare();
        custom_spritesets: [s_fences_and_underlay];
        sprite_layouts: ${sprite_layouts};
        ${misc}
    }
}
""")

item_templates["yard"] = Template("""
switch(FEAT_STATIONS, SELF, sw_item_${name}_prepare, [
    ${temps}
]){return;}
item(FEAT_STATIONS, i_${name}){
    property {
        class: "${class_label}";
        classname: string(STR_CLASS_${class_label});
        name: string(STR_STAT_${name_label});
        tile_flags: [""" + ",\n".join("bitmask(STAT_TILE_NOWIRE)" for i in range(8)) +
"""            ];
    } graphics {
        prepare_layout: sw_item_${name}_prepare();
        custom_spritesets: [s_fences_and_underlay];
        sprite_layouts: ${sprite_layouts};
        ${misc}
    }
}
""")

spritegroup_templates = {}
spritegroup_templates["default"] = Template(""""
spriteset(s_cargo_boxes_few, ZOOM_LEVEL_NORMAL, BIT_DEPTH_8BPP) {
    ${template}(0, 0, "${path}")
    ${template}(1, 0, "${path}")
    ${template}(2, 0, "${path}")
    ${template}(3, 0, "${path}")
    ${template}(4, 0, "${path}")
    ${template}(5, 0, "${path}")
    ${template}(6, 0, "${path}")
    ${template}(7, 0, "${path}")
}

spriteset(s_cargo_boxes_little, ZOOM_LEVEL_NORMAL, BIT_DEPTH_8BPP) {
    ${template}(0, 1, "${path}")
    ${template}(1, 1, "${path}")
    ${template}(2, 1, "${path}")
    ${template}(3, 1, "${path}")
    ${template}(4, 1, "${path}")
    ${template}(5, 1, "${path}")
    ${template}(6, 1, "${path}")
    ${template}(7, 1, "${path}")
}

spriteset(s_cargo_boxes_lots, ZOOM_LEVEL_NORMAL, BIT_DEPTH_8BPP) {
    ${template}(0, 2, "${path}")
    ${template}(1, 2, "${path}")
    ${template}(2, 2, "${path}")
    ${template}(3, 2, "${path}")
    ${template}(4, 2, "${path}")
    ${template}(5, 2, "${path}")
    ${template}(6, 2, "${path}")
    ${template}(7, 2, "${path}")
}
spritegroup sg_${name}_0 {
    little: [s_none, s_none, s_none, s_none,
             s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few,
             s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little,
    ];
    lots: [s_${name}_lots];
}
spritegroup sg_${name}_1 {
    little: [s_none, s_none, s_none,
             s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few,
             s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little,
             s_${name}_lots,
    ];
    lots: [s_${name}_lots];
}
spritegroup sg_${name}_2 {
    little: [s_none, s_none,
             s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few,
             s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little,
             s_${name}_lots, s_${name}_lots,
    ];
    lots: [s_${name}_lots];
}
spritegroup sg_${name}_3 {
    little: [s_none,
             s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few, s_${name}_few,
             s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little, s_${name}_little,
             s_${name}_lots, s_${name}_lots, s_${name}_lots,
    ];
    lots: [s_${name}_lots];
}

random_switch(4, TILE, rsw_${name}, bitmask(TRIGGER_STATION_NEW_CARGO, TRIGGER_STATION_NO_MORE_CARGO)) {
    1: sg_${name}_0;
    1: sg_${name}_1;
    1: sg_${name}_2;
    1: sg_${name}_3;
}
""")
