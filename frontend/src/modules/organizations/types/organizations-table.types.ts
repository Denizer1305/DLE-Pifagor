import type { OrganizationEntityKey, StatusTone } from "./organizations-view.types";

export type TableColumnAlign = "left" | "center" | "right";

export interface OrganizationTableColumn {
    key: string;
    label: string;
    width?: string;
    align?: TableColumnAlign;
    isSortable?: boolean;
    isHiddenOnMobile?: boolean;
}

export type OrganizationTableActionKey =
    | "details"
    | "edit"
    | "archive"
    | "deactivate"
    | "restore"
    | "delete"
    | "setCode"
    | "disableCode"
    | "clearCode"
    | "setPrimary"
    | "approve"
    | "reject";

export interface OrganizationTableAction {
    key: OrganizationTableActionKey;
    label: string;
    icon: string;
    tone: StatusTone;
    isDanger?: boolean;
}

export interface OrganizationTableConfig {
    entity: OrganizationEntityKey;
    columns: OrganizationTableColumn[];
    actions: OrganizationTableAction[];
}

export interface OrganizationTableState {
    isLoading: boolean;
    isRefreshing: boolean;
    selectedId: number | null;
    totalCount: number;
}

export interface OrganizationPaginationState {
    page: number;
    pageSize: number;
    totalCount: number;
    hasNext: boolean;
    hasPrevious: boolean;
}