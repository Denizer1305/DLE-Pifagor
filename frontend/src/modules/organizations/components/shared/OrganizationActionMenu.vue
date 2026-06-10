<script setup lang="ts">
import type { OrganizationTableAction } from "../../types";

interface Props {
    actions: OrganizationTableAction[];
    disabledActions?: string[];
    isDisabled?: boolean;
}

interface Emits {
    (event: "action", actionKey: OrganizationTableAction["key"]): void;
}

const props = withDefaults(defineProps<Props>(), {
    disabledActions: () => [],
    isDisabled: false,
});

defineEmits<Emits>();

function isActionDisabled(action: OrganizationTableAction): boolean {
    return props.isDisabled || props.disabledActions.includes(action.key);
}

function getActionIcon(action: OrganizationTableAction): string {
    const icons: Record<OrganizationTableAction["key"], string> = {
        approve: "fas fa-check",
        archive: "fas fa-box-archive",
        clearCode: "fas fa-eraser",
        deactivate: "fas fa-ban",
        delete: "fas fa-trash",
        details: "fas fa-eye",
        disableCode: "fas fa-key",
        edit: "fas fa-pen",
        reject: "fas fa-xmark",
        restore: "fas fa-rotate-left",
        setCode: "fas fa-key",
        setPrimary: "fas fa-star",
    };

    return icons[action.key] ?? "fas fa-circle";
}
</script>

<template>
    <div class="org-table__actions">
        <button
            v-for="action in actions"
            :key="action.key"
            class="org-table__action"
            :class="{ 'org-table__action--danger': action.isDanger }"
            type="button"
            :disabled="isActionDisabled(action)"
            :title="action.label"
            @click="$emit('action', action.key)"
        >
            <slot
                name="icon"
                :action="action"
            >
                <i :class="getActionIcon(action)"></i>
            </slot>
        </button>
    </div>
</template>
