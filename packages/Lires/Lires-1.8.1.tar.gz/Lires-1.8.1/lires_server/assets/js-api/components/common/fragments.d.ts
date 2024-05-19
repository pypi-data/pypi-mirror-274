export declare const FileSelectButton: import("vue").DefineComponent<{
    asLink: {
        type: BooleanConstructor;
        default: boolean;
    };
    text: {
        type: StringConstructor;
        default: string;
    };
    action: {
        type: FunctionConstructor;
        required: true;
    };
    style: {
        type: ObjectConstructor;
        default: () => {};
    };
}, () => any, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, import("vue").EmitsOptions, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    asLink: {
        type: BooleanConstructor;
        default: boolean;
    };
    text: {
        type: StringConstructor;
        default: string;
    };
    action: {
        type: FunctionConstructor;
        required: true;
    };
    style: {
        type: ObjectConstructor;
        default: () => {};
    };
}>>, {
    text: string;
    style: Record<string, any>;
    asLink: boolean;
}, {}>;
export declare const TextInputWindow: import("vue").DefineComponent<{
    action: {
        type: FunctionConstructor;
        required: true;
    };
    show: {
        type: BooleanConstructor;
        required: true;
    };
    title: {
        type: StringConstructor;
        default: string;
    };
    text: {
        type: StringConstructor;
        default: string;
    };
    placeholder: {
        type: StringConstructor;
        default: string;
    };
    buttonText: {
        type: StringConstructor;
        default: string;
    };
}, () => any, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, import("vue").EmitsOptions, "update:show", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    action: {
        type: FunctionConstructor;
        required: true;
    };
    show: {
        type: BooleanConstructor;
        required: true;
    };
    title: {
        type: StringConstructor;
        default: string;
    };
    text: {
        type: StringConstructor;
        default: string;
    };
    placeholder: {
        type: StringConstructor;
        default: string;
    };
    buttonText: {
        type: StringConstructor;
        default: string;
    };
}>>, {
    title: string;
    text: string;
    placeholder: string;
    buttonText: string;
}, {}>;
export declare const EditableParagraph: import("vue").DefineComponent<{
    contentEditable: {
        type: BooleanConstructor;
        default: boolean;
    };
    style: {
        type: ObjectConstructor;
        default: () => {};
    };
}, () => any, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, import("vue").EmitsOptions, "change" | "finish", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    contentEditable: {
        type: BooleanConstructor;
        default: boolean;
    };
    style: {
        type: ObjectConstructor;
        default: () => {};
    };
}>>, {
    style: Record<string, any>;
    contentEditable: boolean;
}, {}>;
export declare const MenuAttached: import("vue").DefineComponent<{
    menuItems: {
        type: ArrayConstructor;
        required: true;
    };
}, () => any, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, import("vue").EmitsOptions, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    menuItems: {
        type: ArrayConstructor;
        required: true;
    };
}>>, {}, {}>;
export declare const CircularImage: import("vue").DefineComponent<{
    href: {
        type: StringConstructor;
        required: true;
    };
    size: {
        type: StringConstructor;
        required: true;
    };
    alt: {
        type: StringConstructor;
        default: string;
    };
}, () => any, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, import("vue").EmitsOptions, "click", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    href: {
        type: StringConstructor;
        required: true;
    };
    size: {
        type: StringConstructor;
        required: true;
    };
    alt: {
        type: StringConstructor;
        default: string;
    };
}>>, {
    alt: string;
}, {}>;
