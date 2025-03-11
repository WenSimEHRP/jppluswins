from string import Template

item_templates = {}
item_templates["default"] = Template("""
switch(FEAT_STATIONS, SELF, sw_item_${name}_prepare, [
    ${temps}
]){return;}
item(FEAT_STATIONS, i_${name}){
    property {
        class: "${class_label}";
        classname: string(STR_GRF_NAME);
        name: string(STR_GRF_NAME);
        tile_flags: [""" + ",\n".join("bitmask(STAT_TILE_PYLON)" for i in range(8)) +
"""            ];
    } graphics {
        prepare_layout: sw_item_${name}_prepare();
        custom_spritesets: [s_fences_and_underlay];
        sprite_layouts: [sp_${name}_x, sp_${name}_y];
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
        classname: string(STR_GRF_NAME);
        name: string(STR_GRF_NAME);
        tile_flags: [""" + ",\n".join("bitmask()" for i in range(8)) +
"""            ];
    } graphics {
        prepare_layout: sw_item_${name}_prepare();
        custom_spritesets: [s_fences_and_underlay];
        sprite_layouts: [sp_${name}_x, sp_${name}_y];
    }
}
""")
