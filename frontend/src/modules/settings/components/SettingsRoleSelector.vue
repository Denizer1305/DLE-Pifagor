<script setup lang="ts">
import type { SettingsRoleCode } from "@/modules/settings/types/settings.types";

interface RoleOption {
    key: SettingsRoleCode;
    icon: string;
    label: string;
}

interface Props {
    activeRole: SettingsRoleCode;
    options: RoleOption[];
    disabled?: boolean;
}

interface Emits {
    (event: "select", value: SettingsRoleCode): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <div class="role-settings-role-grid">
        <button
            v-for="role in options"
            :key="role.key"
            type="button"
            class="role-settings-role-option"
            :class="{ 'is-active': role.key === activeRole }"
            :disabled="disabled"
            @click="emit('select', role.key)"
        >
            <i :class="role.icon"></i>
            <span>{{ role.label }}</span>
        </button>
    </div>
</template>
