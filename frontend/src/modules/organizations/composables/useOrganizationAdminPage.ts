import { computed } from "vue";
import { useRoute } from "vue-router";

import {
    ORGANIZATION_ADMIN_PAGE_HEADER,
    ORGANIZATION_ENTITY_HEADERS,
    ORGANIZATION_EMPTY_STATES,
    ORGANIZATIONS_NAVIGATION,
    ORGANIZATION_SUMMARY_PLACEHOLDERS,
    ORGANIZATION_TABLE_CONFIGS,
} from "../data";
import { ORGANIZATION_ROUTE_NAMES } from "../utils";
import type {
    OrganizationEntityKey,
    OrganizationNavigationItem,
} from "../types";

const DEFAULT_ENTITY: OrganizationEntityKey = "organizations";

function getEntityByRouteName(routeName: string | symbol | null | undefined): OrganizationEntityKey {
    const normalizedRouteName = String(routeName || "");

    const matchedEntry = Object.entries(ORGANIZATION_ROUTE_NAMES).find(
        ([, currentRouteName]) => {
            return currentRouteName === normalizedRouteName;
        },
    );

    if (!matchedEntry) {
        return DEFAULT_ENTITY;
    }

    return matchedEntry[0] as OrganizationEntityKey;
}

export function useOrganizationAdminPage() {
    const route = useRoute();

    const activeEntity = computed<OrganizationEntityKey>(() => {
        return getEntityByRouteName(route.name);
    });

    const pageHeader = computed(() => {
        return ORGANIZATION_ENTITY_HEADERS[activeEntity.value];
    });

    const rootHeader = computed(() => {
        return ORGANIZATION_ADMIN_PAGE_HEADER;
    });

    const navigation = computed<OrganizationNavigationItem[]>(() => {
        return ORGANIZATIONS_NAVIGATION.map((item) => {
            return {
                ...item,
                badge: item.badge,
            };
        });
    });

    const summary = computed(() => {
        return ORGANIZATION_SUMMARY_PLACEHOLDERS;
    });

    const tableConfig = computed(() => {
        return ORGANIZATION_TABLE_CONFIGS[activeEntity.value];
    });

    const emptyState = computed(() => {
        return ORGANIZATION_EMPTY_STATES[activeEntity.value];
    });

    const activeNavigationItem = computed(() => {
        return navigation.value.find((item) => {
            return item.key === activeEntity.value;
        }) ?? navigation.value[0];
    });

    return {
        activeEntity,
        activeNavigationItem,
        emptyState,
        navigation,
        pageHeader,
        rootHeader,
        summary,
        tableConfig,
    };
}
