export type BibtexTypes = 'article' | 'inproceedings' | 'webpage' | 'misc';
export declare const getBibtexTemplate: (type: BibtexTypes, { entry, title, authors, year, }?: {
    entry?: string;
    title?: string;
    authors?: string[];
    year?: number;
}) => string;
interface CollectRes {
    bibtex: string;
    url: string;
}
export declare class BibtexCollector {
    static fromArxiv(query: string): Promise<CollectRes>;
    static fromWebpage(url: string): Promise<CollectRes>;
    static fromDoi(doi: string): Promise<CollectRes>;
}
export {};
