import type { DataInfoT, FeedDataInfoT, UserInfo, SearchType, SearchResult, Changelog, ServerStatus, DatabaseFeature, DatabaseUsage } from "./protocol.js";
import Fetcher from "./fetcher";
/**
 * Resolve the path of the resources on the server,
 * these resources are the files that can be accessed by the get request.
 * NOT USED IN THE CURRENT VERSION
 */
export declare class HTTPPathResolver {
    private baseURLGetter;
    private tokenGetter;
    constructor(baseURLGetter: () => string, tokenGetter?: () => string);
    get baseURL(): string;
    get token(): string;
    doc(uid: string, userID: number): string;
    docDry: (uid: string, userID: number) => string;
    docText: (uid: string, userID: number) => string;
    databaseDownload(data?: boolean): string;
    miscFile(uid: string, fname: string): string;
    userAvatar(username: string, opt?: {
        size: number;
        t: number | null;
    }): string;
}
/**
 * Properties:
 *  - resolve: resolve the path of the resources on the server
 *
 * Naming convention:
 *  - req...: request data from server
 *  - update...: update data on the server
 *  - delete...: delete data on the server
 *  - upload...: upload files
 *  - [Other]: functional methods that do not fit the above categories
 */
export declare class ServerConn {
    fetcher: Fetcher;
    resolve: HTTPPathResolver;
    constructor(baseUrlGetter: () => string, tokenGetter: () => string, sessionIDGetter?: (() => string) | null);
    get baseURL(): string;
    authorize(): Promise<UserInfo>;
    status(): Promise<ServerStatus>;
    reqAllKeys(): Promise<string[]>;
    reqAllTags(): Promise<string[]>;
    reqDatabaseFeatureTSNE(collectionName?: string, nComponent?: number, perplexity?: number): Promise<DatabaseFeature>;
    reqDatabaseUsage(): Promise<DatabaseUsage>;
    reqDatapointSummary(uid: string): Promise<DataInfoT>;
    reqDatapointSummaries(uids: string[]): Promise<DataInfoT[]>;
    deleteDatapoint(uid: string): Promise<boolean>;
    /**
        * Create or update a datapoint
        * @param uid: the uid of the datapoint to update, if null, create a new datapoint
        * @param bibtex: the bibtex content
        * @param tags: the tags of the datapoint
        * @param url: the url of the datapoint
        * @return the updated datapoint
    */
    updateDatapoint(uid: string | null, { bibtex, tags, url, }: {
        bibtex?: string | null;
        tags?: string[] | null;
        url?: string | null;
    }): Promise<DataInfoT>;
    reqDatapointAbstract(uid: string): Promise<string>;
    updateDatapointAbstract(uid: string, content: string): Promise<boolean>;
    reqDatapointNote(uid: string): Promise<string>;
    updateDatapointNote(uid: string, content: string): Promise<boolean>;
    query({ tags, searchBy, searchContent, maxResults, }?: {
        tags?: string[];
        searchBy?: SearchType;
        searchContent?: string;
        maxResults?: number;
    }): Promise<SearchResult>;
    featurizeText(text: string, requireCache?: boolean): Promise<number[]>;
    reqAISummary(uid: string, onStreamComing: (txt: string) => void, onDone?: () => void, force?: boolean, model?: string): void;
    reqMiscFileList(uid: string): Promise<string[]>;
    deleteMiscFile(uid: string, fileName: string): Promise<boolean>;
    renameMiscFile(uid: string, fileName: string, newFileName: string): Promise<boolean>;
    uploadMiscFiles(uid: string, files: File[]): Promise<string[]>;
    uploadDocument(uid: string, file: File): Promise<DataInfoT>;
    deleteDocument(uid: string): Promise<DataInfoT>;
    updateTagAll(oldTag: string, newTag: string): Promise<boolean>;
    deleteTagAll(tag: string): Promise<boolean>;
    reqUserInfo(username: string): Promise<UserInfo>;
    updateUserNickname(name: string): Promise<UserInfo>;
    updateUserPassword(newPassword: string): Promise<UserInfo>;
    reqUserList(): Promise<UserInfo[]>;
    uploadUserAvatar(username: string, file: File): Promise<UserInfo>;
    updateUserAccess(username: string, setAdmin: boolean | null, setMandatoryTags: string[] | null, max_storage: number | null): Promise<UserInfo>;
    registerUser(invitation_code: string, username: string, password: string, name: string): Promise<UserInfo>;
    createUser(username: string, name: string, password: string, isAdmin: boolean, mandatoryTags: string[], max_storage: number): Promise<UserInfo>;
    deleteUser(username: string): Promise<boolean>;
    reqFeedList({ maxResults, category, timeBefore, timeAfter, }: {
        maxResults?: number;
        category?: string;
        timeBefore?: number;
        timeAfter?: number;
    }): Promise<FeedDataInfoT[]>;
    reqFeedCategories(): Promise<string[]>;
    changelog(): Promise<Changelog>;
}
export default ServerConn;
