import { BBox } from "./util/bbox";
import type { Size, Box, Extents, PlainObject } from "./types";
import type { CSSStyles, CSSStyleSheetDecl } from "./css";
type Optional<T> = {
    [P in keyof T]?: T[P] | null | undefined;
};
type HTMLElementName = keyof HTMLElementTagNameMap;
type CSSClass = string;
type ElementOurAttrs = {
    class?: CSSClass | (CSSClass | null | undefined)[];
    style?: CSSStyles;
    data?: PlainObject<string | null | undefined>;
};
type ElementCommonAttrs = {
    title: HTMLElement["title"];
    tabIndex: HTMLOrSVGElement["tabIndex"];
};
export type HTMLAttrs<_T extends HTMLElementName, ElementSpecificAttrs> = ElementOurAttrs & Optional<ElementCommonAttrs> & Optional<ElementSpecificAttrs>;
export type HTMLItem = string | Node | NodeList | HTMLCollection | null | undefined;
export type HTMLChild = HTMLItem | HTMLItem[];
export declare function create_element<T extends keyof HTMLElementTagNameMap>(tag: T, attrs: HTMLAttrs<T, {}> | null, ...children: HTMLChild[]): HTMLElementTagNameMap[T];
export declare const a: (attrs?: HTMLChild | HTMLAttrs<"a", {
    href: HTMLAnchorElement["href"];
    target: HTMLAnchorElement["target"];
}>, ...children: HTMLChild[]) => HTMLAnchorElement;
export declare const abbr: (attrs?: HTMLChild | HTMLAttrs<"abbr", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const address: (attrs?: HTMLChild | HTMLAttrs<"address", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const area: (attrs?: HTMLChild | HTMLAttrs<"area", {}>, ...children: HTMLChild[]) => HTMLAreaElement;
export declare const article: (attrs?: HTMLChild | HTMLAttrs<"article", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const aside: (attrs?: HTMLChild | HTMLAttrs<"aside", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const audio: (attrs?: HTMLChild | HTMLAttrs<"audio", {}>, ...children: HTMLChild[]) => HTMLAudioElement;
export declare const b: (attrs?: HTMLChild | HTMLAttrs<"b", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const base: (attrs?: HTMLChild | HTMLAttrs<"base", {}>, ...children: HTMLChild[]) => HTMLBaseElement;
export declare const bdi: (attrs?: HTMLChild | HTMLAttrs<"bdi", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const bdo: (attrs?: HTMLChild | HTMLAttrs<"bdo", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const blockquote: (attrs?: HTMLChild | HTMLAttrs<"blockquote", {}>, ...children: HTMLChild[]) => HTMLQuoteElement;
export declare const body: (attrs?: HTMLChild | HTMLAttrs<"body", {}>, ...children: HTMLChild[]) => HTMLBodyElement;
export declare const br: (attrs?: HTMLChild | HTMLAttrs<"br", {}>, ...children: HTMLChild[]) => HTMLBRElement;
export declare const button: (attrs?: HTMLChild | HTMLAttrs<"button", {
    type: "button";
    disabled: HTMLButtonElement["disabled"];
}>, ...children: HTMLChild[]) => HTMLButtonElement;
export declare const canvas: (attrs?: HTMLChild | HTMLAttrs<"canvas", {
    width: HTMLCanvasElement["width"];
    height: HTMLCanvasElement["height"];
}>, ...children: HTMLChild[]) => HTMLCanvasElement;
export declare const caption: (attrs?: HTMLChild | HTMLAttrs<"caption", {}>, ...children: HTMLChild[]) => HTMLTableCaptionElement;
export declare const cite: (attrs?: HTMLChild | HTMLAttrs<"cite", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const code: (attrs?: HTMLChild | HTMLAttrs<"code", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const col: (attrs?: HTMLChild | HTMLAttrs<"col", {}>, ...children: HTMLChild[]) => HTMLTableColElement;
export declare const colgroup: (attrs?: HTMLChild | HTMLAttrs<"colgroup", {}>, ...children: HTMLChild[]) => HTMLTableColElement;
export declare const data: (attrs?: HTMLChild | HTMLAttrs<"data", {}>, ...children: HTMLChild[]) => HTMLDataElement;
export declare const datalist: (attrs?: HTMLChild | HTMLAttrs<"datalist", {}>, ...children: HTMLChild[]) => HTMLDataListElement;
export declare const dd: (attrs?: HTMLChild | HTMLAttrs<"dd", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const del: (attrs?: HTMLChild | HTMLAttrs<"del", {}>, ...children: HTMLChild[]) => HTMLModElement;
export declare const details: (attrs?: HTMLChild | HTMLAttrs<"details", {}>, ...children: HTMLChild[]) => HTMLDetailsElement;
export declare const dfn: (attrs?: HTMLChild | HTMLAttrs<"dfn", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const dialog: (attrs?: HTMLChild | HTMLAttrs<"dialog", {}>, ...children: HTMLChild[]) => HTMLDialogElement;
export declare const div: (attrs?: HTMLChild | HTMLAttrs<"div", {}>, ...children: HTMLChild[]) => HTMLDivElement;
export declare const dl: (attrs?: HTMLChild | HTMLAttrs<"dl", {}>, ...children: HTMLChild[]) => HTMLDListElement;
export declare const dt: (attrs?: HTMLChild | HTMLAttrs<"dt", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const em: (attrs?: HTMLChild | HTMLAttrs<"em", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const embed: (attrs?: HTMLChild | HTMLAttrs<"embed", {}>, ...children: HTMLChild[]) => HTMLEmbedElement;
export declare const fieldset: (attrs?: HTMLChild | HTMLAttrs<"fieldset", {}>, ...children: HTMLChild[]) => HTMLFieldSetElement;
export declare const figcaption: (attrs?: HTMLChild | HTMLAttrs<"figcaption", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const figure: (attrs?: HTMLChild | HTMLAttrs<"figure", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const footer: (attrs?: HTMLChild | HTMLAttrs<"footer", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const form: (attrs?: HTMLChild | HTMLAttrs<"form", {}>, ...children: HTMLChild[]) => HTMLFormElement;
export declare const h1: (attrs?: HTMLChild | HTMLAttrs<"h1", {}>, ...children: HTMLChild[]) => HTMLHeadingElement;
export declare const h2: (attrs?: HTMLChild | HTMLAttrs<"h2", {}>, ...children: HTMLChild[]) => HTMLHeadingElement;
export declare const h3: (attrs?: HTMLChild | HTMLAttrs<"h3", {}>, ...children: HTMLChild[]) => HTMLHeadingElement;
export declare const h4: (attrs?: HTMLChild | HTMLAttrs<"h4", {}>, ...children: HTMLChild[]) => HTMLHeadingElement;
export declare const h5: (attrs?: HTMLChild | HTMLAttrs<"h5", {}>, ...children: HTMLChild[]) => HTMLHeadingElement;
export declare const h6: (attrs?: HTMLChild | HTMLAttrs<"h6", {}>, ...children: HTMLChild[]) => HTMLHeadingElement;
export declare const head: (attrs?: HTMLChild | HTMLAttrs<"head", {}>, ...children: HTMLChild[]) => HTMLHeadElement;
export declare const header: (attrs?: HTMLChild | HTMLAttrs<"header", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const hgroup: (attrs?: HTMLChild | HTMLAttrs<"hgroup", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const hr: (attrs?: HTMLChild | HTMLAttrs<"hr", {}>, ...children: HTMLChild[]) => HTMLHRElement;
export declare const html: (attrs?: HTMLChild | HTMLAttrs<"html", {}>, ...children: HTMLChild[]) => HTMLHtmlElement;
export declare const i: (attrs?: HTMLChild | HTMLAttrs<"i", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const iframe: (attrs?: HTMLChild | HTMLAttrs<"iframe", {}>, ...children: HTMLChild[]) => HTMLIFrameElement;
export declare const img: (attrs?: HTMLChild | HTMLAttrs<"img", {}>, ...children: HTMLChild[]) => HTMLImageElement;
export declare const input: (attrs?: HTMLChild | HTMLAttrs<"input", {
    type: "text" | "checkbox" | "radio" | "file" | "color";
    name: HTMLInputElement["name"];
    multiple: HTMLInputElement["multiple"];
    disabled: HTMLInputElement["disabled"];
    checked: HTMLInputElement["checked"];
    placeholder: HTMLInputElement["placeholder"];
    accept: HTMLInputElement["accept"];
    value: HTMLInputElement["value"];
    readonly: HTMLInputElement["readOnly"];
}>, ...children: HTMLChild[]) => HTMLInputElement;
export declare const ins: (attrs?: HTMLChild | HTMLAttrs<"ins", {}>, ...children: HTMLChild[]) => HTMLModElement;
export declare const kbd: (attrs?: HTMLChild | HTMLAttrs<"kbd", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const label: (attrs?: HTMLChild | HTMLAttrs<"label", {
    for: HTMLLabelElement["htmlFor"];
}>, ...children: HTMLChild[]) => HTMLLabelElement;
export declare const legend: (attrs?: HTMLChild | HTMLAttrs<"legend", {}>, ...children: HTMLChild[]) => HTMLLegendElement;
export declare const li: (attrs?: HTMLChild | HTMLAttrs<"li", {}>, ...children: HTMLChild[]) => HTMLLIElement;
export declare const link: (attrs?: HTMLChild | HTMLAttrs<"link", {
    rel: HTMLLinkElement["rel"];
    href: HTMLLinkElement["href"];
    disabled: HTMLLinkElement["disabled"];
}>, ...children: HTMLChild[]) => HTMLLinkElement;
export declare const main: (attrs?: HTMLChild | HTMLAttrs<"main", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const map: (attrs?: HTMLChild | HTMLAttrs<"map", {}>, ...children: HTMLChild[]) => HTMLMapElement;
export declare const mark: (attrs?: HTMLChild | HTMLAttrs<"mark", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const menu: (attrs?: HTMLChild | HTMLAttrs<"menu", {}>, ...children: HTMLChild[]) => HTMLMenuElement;
export declare const meta: (attrs?: HTMLChild | HTMLAttrs<"meta", {}>, ...children: HTMLChild[]) => HTMLMetaElement;
export declare const meter: (attrs?: HTMLChild | HTMLAttrs<"meter", {}>, ...children: HTMLChild[]) => HTMLMeterElement;
export declare const nav: (attrs?: HTMLChild | HTMLAttrs<"nav", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const noscript: (attrs?: HTMLChild | HTMLAttrs<"noscript", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const object: (attrs?: HTMLChild | HTMLAttrs<"object", {}>, ...children: HTMLChild[]) => HTMLObjectElement;
export declare const ol: (attrs?: HTMLChild | HTMLAttrs<"ol", {}>, ...children: HTMLChild[]) => HTMLOListElement;
export declare const optgroup: (attrs?: HTMLChild | HTMLAttrs<"optgroup", {
    disabled: HTMLOptGroupElement["disabled"];
    label: HTMLOptGroupElement["label"];
}>, ...children: HTMLChild[]) => HTMLOptGroupElement;
export declare const option: (attrs?: HTMLChild | HTMLAttrs<"option", {
    value: HTMLOptionElement["value"];
}>, ...children: HTMLChild[]) => HTMLOptionElement;
export declare const output: (attrs?: HTMLChild | HTMLAttrs<"output", {}>, ...children: HTMLChild[]) => HTMLOutputElement;
export declare const p: (attrs?: HTMLChild | HTMLAttrs<"p", {}>, ...children: HTMLChild[]) => HTMLParagraphElement;
export declare const picture: (attrs?: HTMLChild | HTMLAttrs<"picture", {}>, ...children: HTMLChild[]) => HTMLPictureElement;
export declare const pre: (attrs?: HTMLChild | HTMLAttrs<"pre", {}>, ...children: HTMLChild[]) => HTMLPreElement;
export declare const progress: (attrs?: HTMLChild | HTMLAttrs<"progress", {}>, ...children: HTMLChild[]) => HTMLProgressElement;
export declare const q: (attrs?: HTMLChild | HTMLAttrs<"q", {}>, ...children: HTMLChild[]) => HTMLQuoteElement;
export declare const rp: (attrs?: HTMLChild | HTMLAttrs<"rp", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const rt: (attrs?: HTMLChild | HTMLAttrs<"rt", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const ruby: (attrs?: HTMLChild | HTMLAttrs<"ruby", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const s: (attrs?: HTMLChild | HTMLAttrs<"s", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const samp: (attrs?: HTMLChild | HTMLAttrs<"samp", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const script: (attrs?: HTMLChild | HTMLAttrs<"script", {}>, ...children: HTMLChild[]) => HTMLScriptElement;
export declare const search: (attrs?: HTMLChild | HTMLAttrs<"search", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const section: (attrs?: HTMLChild | HTMLAttrs<"section", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const select: (attrs?: HTMLChild | HTMLAttrs<"select", {
    name: HTMLSelectElement["name"];
    disabled: HTMLSelectElement["disabled"];
    multiple: HTMLSelectElement["multiple"];
}>, ...children: HTMLChild[]) => HTMLSelectElement;
export declare const slot: (attrs?: HTMLChild | HTMLAttrs<"slot", {}>, ...children: HTMLChild[]) => HTMLSlotElement;
export declare const small: (attrs?: HTMLChild | HTMLAttrs<"small", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const source: (attrs?: HTMLChild | HTMLAttrs<"source", {}>, ...children: HTMLChild[]) => HTMLSourceElement;
export declare const span: (attrs?: HTMLChild | HTMLAttrs<"span", {}>, ...children: HTMLChild[]) => HTMLSpanElement;
export declare const strong: (attrs?: HTMLChild | HTMLAttrs<"strong", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const style: (attrs?: HTMLChild | HTMLAttrs<"style", {}>, ...children: HTMLChild[]) => HTMLStyleElement;
export declare const sub: (attrs?: HTMLChild | HTMLAttrs<"sub", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const summary: (attrs?: HTMLChild | HTMLAttrs<"summary", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const sup: (attrs?: HTMLChild | HTMLAttrs<"sup", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const table: (attrs?: HTMLChild | HTMLAttrs<"table", {}>, ...children: HTMLChild[]) => HTMLTableElement;
export declare const tbody: (attrs?: HTMLChild | HTMLAttrs<"tbody", {}>, ...children: HTMLChild[]) => HTMLTableSectionElement;
export declare const td: (attrs?: HTMLChild | HTMLAttrs<"td", {}>, ...children: HTMLChild[]) => HTMLTableCellElement;
export declare const template: (attrs?: HTMLChild | HTMLAttrs<"template", {}>, ...children: HTMLChild[]) => HTMLTemplateElement;
export declare const textarea: (attrs?: HTMLChild | HTMLAttrs<"textarea", {}>, ...children: HTMLChild[]) => HTMLTextAreaElement;
export declare const tfoot: (attrs?: HTMLChild | HTMLAttrs<"tfoot", {}>, ...children: HTMLChild[]) => HTMLTableSectionElement;
export declare const th: (attrs?: HTMLChild | HTMLAttrs<"th", {}>, ...children: HTMLChild[]) => HTMLTableCellElement;
export declare const thead: (attrs?: HTMLChild | HTMLAttrs<"thead", {}>, ...children: HTMLChild[]) => HTMLTableSectionElement;
export declare const time: (attrs?: HTMLChild | HTMLAttrs<"time", {}>, ...children: HTMLChild[]) => HTMLTimeElement;
export declare const title: (attrs?: HTMLChild | HTMLAttrs<"title", {}>, ...children: HTMLChild[]) => HTMLTitleElement;
export declare const tr: (attrs?: HTMLChild | HTMLAttrs<"tr", {}>, ...children: HTMLChild[]) => HTMLTableRowElement;
export declare const track: (attrs?: HTMLChild | HTMLAttrs<"track", {}>, ...children: HTMLChild[]) => HTMLTrackElement;
export declare const u: (attrs?: HTMLChild | HTMLAttrs<"u", {}>, ...children: HTMLChild[]) => HTMLElement;
export declare const ul: (attrs?: HTMLChild | HTMLAttrs<"ul", {}>, ...children: HTMLChild[]) => HTMLUListElement;
export declare const video: (attrs?: HTMLChild | HTMLAttrs<"video", {}>, ...children: HTMLChild[]) => HTMLVideoElement;
export declare const wbr: (attrs?: HTMLChild | HTMLAttrs<"wbr", {}>, ...children: HTMLChild[]) => HTMLElement;
export type SVGAttrs = {
    [key: string]: string | false | null | undefined;
};
export declare function createSVGElement<T extends keyof SVGElementTagNameMap>(tag: T, attrs?: SVGAttrs | null, ...children: HTMLChild[]): SVGElementTagNameMap[T];
export declare function text(str: string): Text;
export declare function nbsp(): Text;
export declare function prepend(element: Node, ...nodes: Node[]): void;
export declare function empty(node: Node, attrs?: boolean): void;
export declare function contains(element: Element, child: Node): boolean;
export declare function display(element: HTMLElement, display?: boolean): void;
export declare function undisplay(element: HTMLElement): void;
export declare function show(element: HTMLElement): void;
export declare function hide(element: HTMLElement): void;
export declare function offset_bbox(element: Element): BBox;
export declare function parent(el: HTMLElement, selector: string): HTMLElement | null;
export type ElementExtents = {
    border: Extents;
    margin: Extents;
    padding: Extents;
};
export declare function extents(el: HTMLElement): ElementExtents;
export declare function size(el: HTMLElement): Size;
export declare function scroll_size(el: HTMLElement): Size;
export declare function outer_size(el: HTMLElement): Size;
export declare function content_size(el: HTMLElement): Size;
export declare function bounding_box(el: Element): BBox;
export declare function box_size(el: Element): Size;
export declare function position(el: HTMLElement, box: Box, margin?: Extents): void;
export declare class ClassList {
    private readonly class_list;
    constructor(class_list: DOMTokenList);
    get values(): string[];
    has(cls: string): boolean;
    add(...classes: string[]): this;
    remove(...classes: string[] | string[][]): this;
    clear(): this;
    toggle(cls: string, activate?: boolean): this;
}
export declare function classes(el: HTMLElement): ClassList;
export declare function toggle_attribute(el: HTMLElement, attr: string, state?: boolean): void;
type WhitespaceKeys = "Tab" | "Enter" | " ";
type UIKeys = "Escape";
type NavigationKeys = "Home" | "End" | "PageUp" | "PageDown" | "ArrowLeft" | "ArrowRight" | "ArrowUp" | "ArrowDown";
type EditingKeys = "Backspace" | "Delete";
export type Keys = WhitespaceKeys | UIKeys | NavigationKeys | EditingKeys;
export declare enum MouseButton {
    None = 0,
    Primary = 1,
    Secondary = 2,
    Auxiliary = 4,
    Left = 1,
    Right = 2,
    Middle = 4
}
export declare abstract class StyleSheet {
    protected readonly el: HTMLStyleElement | HTMLLinkElement;
    install(el: HTMLElement | ShadowRoot): void;
    uninstall(): void;
}
export declare class InlineStyleSheet extends StyleSheet {
    protected readonly el: HTMLStyleElement;
    constructor(css?: string | CSSStyleSheetDecl);
    get css(): string;
    protected _update(css: string): void;
    clear(): void;
    private _to_css;
    replace(css: string, styles?: CSSStyles): void;
    prepend(css: string, styles?: CSSStyles): void;
    append(css: string, styles?: CSSStyles): void;
    remove(): void;
}
export declare class GlobalInlineStyleSheet extends InlineStyleSheet {
    install(): void;
}
export declare class ImportedStyleSheet extends StyleSheet {
    protected readonly el: HTMLLinkElement;
    constructor(url: string);
    replace(url: string): void;
    remove(): void;
}
export declare class GlobalImportedStyleSheet extends ImportedStyleSheet {
    install(): void;
}
export type StyleSheetLike = StyleSheet | string;
export declare function dom_ready(): Promise<void>;
export declare function px(value: number | string): string;
export declare const supports_adopted_stylesheets: boolean;
export {};
//# sourceMappingURL=dom.d.ts.map