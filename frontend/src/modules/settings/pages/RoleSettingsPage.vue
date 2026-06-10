<script setup lang="ts">
import { computed } from "vue";

import SettingsPageShell from "@/modules/settings/components/SettingsPageShell.vue";
import SettingsRoleSelector from "@/modules/settings/components/SettingsRoleSelector.vue";
import SettingsSectionCard from "@/modules/settings/components/SettingsSectionCard.vue";
import SettingsToggleRow from "@/modules/settings/components/SettingsToggleRow.vue";

import { useRoleSettings } from "@/modules/settings/composables/useRoleSettings";
import {
    adminRoleOptions,
    guardianRoleOptions,
    learnerRoleOptions,
    settingsRoleOptions,
    settingsRoleTitles,
    teacherRoleOptions,
} from "@/modules/settings/data/role-settings.data";

import type {
    AdminRoleSettingsDto,
    GuardianRoleSettingsDto,
    LearnerRoleSettingsDto,
    TeacherRoleSettingsDto,
} from "@/modules/settings/types/settings.types";

const {
    settings,
    pageState,
    activeRole,
    isLoading,
    isSaving,
    errorMessage,
    loadRoleSettings,
    setActiveRole,
    updateRoleOption,
} = useRoleSettings();

const activeRoleTitle = computed(() => {
    return settingsRoleTitles[activeRole.value];
});

async function updateTeacherOption(
    key: keyof TeacherRoleSettingsDto,
    value: boolean,
): Promise<void> {
    await updateRoleOption("teacher", key, value);
}

async function updateLearnerOption(
    key: keyof LearnerRoleSettingsDto,
    value: boolean,
): Promise<void> {
    await updateRoleOption("learner", key, value);
}

async function updateGuardianOption(
    key: keyof GuardianRoleSettingsDto,
    value: boolean,
): Promise<void> {
    await updateRoleOption("guardian", key, value);
}

async function updateAdminOption(
    key: keyof AdminRoleSettingsDto,
    value: boolean,
): Promise<void> {
    await updateRoleOption("admin", key, value);
}

</script>

<template>
    <SettingsPageShell
        :model="pageState?.scaffold"
        :hero="pageState?.hero"
        :is-ready="Boolean(pageState && settings)"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем ролевые настройки..."
        @reload="loadRoleSettings"
    >
        <template v-if="settings">
        <SettingsSectionCard
            icon="fas fa-users-gear"
            topline="Выбор роли"
            title="Для какой роли настраивается кабинет"
            text="Каждый пользователь может настроить поведение интерфейса под свою роль. Позже здесь появятся дефолты организации и платформы."
        >
            <SettingsRoleSelector
                :active-role="activeRole"
                :options="settingsRoleOptions"
                :disabled="isSaving"
                @select="setActiveRole"
            />
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-table-cells-large"
            topline="Поведение интерфейса"
            :title="activeRoleTitle"
            text="Управляйте тем, какие блоки и панели будут отображаться в личном кабинете выбранной роли."
        >
            <div
                v-if="activeRole === 'teacher'"
                class="settings-toggle-list"
            >
                <SettingsToggleRow
                    v-for="option in teacherRoleOptions"
                    :key="option.key"
                    :label="option.label"
                    :text="option.text"
                    :model-value="settings.roles.teacher[option.key]"
                    :disabled="isSaving"
                    @update:model-value="updateTeacherOption(option.key, $event)"
                />
            </div>

            <div
                v-else-if="activeRole === 'learner'"
                class="settings-toggle-list"
            >
                <SettingsToggleRow
                    v-for="option in learnerRoleOptions"
                    :key="option.key"
                    :label="option.label"
                    :text="option.text"
                    :model-value="settings.roles.learner[option.key]"
                    :disabled="isSaving"
                    @update:model-value="updateLearnerOption(option.key, $event)"
                />
            </div>

            <div
                v-else-if="activeRole === 'guardian'"
                class="settings-toggle-list"
            >
                <SettingsToggleRow
                    v-for="option in guardianRoleOptions"
                    :key="option.key"
                    :label="option.label"
                    :text="option.text"
                    :model-value="settings.roles.guardian[option.key]"
                    :disabled="isSaving"
                    @update:model-value="updateGuardianOption(option.key, $event)"
                />
            </div>

            <div
                v-else
                class="settings-toggle-list"
            >
                <SettingsToggleRow
                    v-for="option in adminRoleOptions"
                    :key="option.key"
                    :label="option.label"
                    :text="option.text"
                    :model-value="settings.roles.admin[option.key]"
                    :disabled="isSaving"
                    @update:model-value="updateAdminOption(option.key, $event)"
                />
            </div>
        </SettingsSectionCard>
        </template>
    </SettingsPageShell>
</template>
