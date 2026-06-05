<script setup lang="ts">
import SettingsPageShell from "@/modules/settings/components/SettingsPageShell.vue";
import SettingsPasswordForm from "@/modules/settings/components/SettingsPasswordForm.vue";
import SettingsSectionCard from "@/modules/settings/components/SettingsSectionCard.vue";
import SettingsSecuritySessions from "@/modules/settings/components/SettingsSecuritySessions.vue";
import SettingsSelectRow from "@/modules/settings/components/SettingsSelectRow.vue";
import SettingsToggleRow from "@/modules/settings/components/SettingsToggleRow.vue";

import { sessionLifetimeOptions } from "@/modules/settings/data/settings-options.data";
import { securityPasswordFormContent } from "@/modules/settings/data/security-settings.data";
import { useSecuritySettings } from "@/modules/settings/composables/useSecuritySettings";

import type {
    PasswordFormState,
    SessionLifetimeMode,
} from "@/modules/settings/types/settings.types";

const {
    settings,
    sessions,
    pageState,
    passwordForm,
    passwordErrors,
    isLoading,
    isSaving,
    isPasswordSubmitting,
    errorMessage,
    successMessage,
    loadSecuritySettings,
    updateSecurity,
    submitPasswordChange,
    logoutAllUserSessions,
    logoutUserSession,
} = useSecuritySettings();

async function updateSessionLifetime(value: string): Promise<void> {
    await updateSecurity({
        session_lifetime_mode: value as SessionLifetimeMode,
    });
}

function updatePasswordField(field: keyof PasswordFormState, value: string): void {
    passwordForm[field] = value;
}

</script>

<template>
    <SettingsPageShell
        :model="pageState?.scaffold"
        :hero="pageState?.hero"
        :is-ready="Boolean(pageState && settings)"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем настройки безопасности..."
        @reload="loadSecuritySettings"
    >
        <template v-if="settings">
        <div
            v-if="successMessage"
            class="settings-success-card"
        >
            <i class="fas fa-circle-check"></i>
            <span>{{ successMessage }}</span>
        </div>

        <SettingsSectionCard
            icon="fas fa-key"
            topline="Пароль"
            title="Смена пароля аккаунта"
            text="Регулярная смена пароля помогает защитить личный кабинет и данные пользователя."
        >
            <SettingsPasswordForm
                :form="passwordForm"
                :errors="passwordErrors"
                :content="securityPasswordFormContent"
                :is-submitting="isPasswordSubmitting"
                @submit="submitPasswordChange"
                @update-field="updatePasswordField"
            />
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-shield-halved"
            topline="Дополнительная защита"
            title="Правила входа и контроля активности"
            text="Эти параметры помогают быстрее узнавать о подозрительной активности и управлять длительностью сессий."
        >
            <div class="settings-toggle-list">
                <SettingsToggleRow
                    label="Уведомления о входе"
                    text="Отправлять уведомления при новом входе в аккаунт."
                    :model-value="settings.login_notifications_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateSecurity({ login_notifications_enabled: $event })"
                />

                <SettingsToggleRow
                    label="Контроль подозрительной активности"
                    text="Показывать предупреждения при необычном поведении аккаунта."
                    :model-value="settings.suspicious_activity_notifications_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateSecurity({ suspicious_activity_notifications_enabled: $event })"
                />

                <SettingsToggleRow
                    label="Доверенные устройства"
                    text="Разрешить платформе запоминать устройства для удобного входа."
                    :model-value="settings.trusted_devices_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateSecurity({ trusted_devices_enabled: $event })"
                />

                <SettingsToggleRow
                    label="Двухфакторная защита"
                    text="Дополнительный уровень защиты аккаунта. Полная 2FA будет расширена отдельным этапом."
                    :model-value="settings.two_factor_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateSecurity({ two_factor_enabled: $event })"
                />
            </div>

            <div class="settings-form-grid">
                <SettingsSelectRow
                    label="Режим длительности сессии"
                    text="Определяет, как долго пользователь остаётся авторизованным."
                    :model-value="settings.session_lifetime_mode"
                    :options="sessionLifetimeOptions"
                    :disabled="isSaving"
                    @update:model-value="updateSessionLifetime"
                />
            </div>
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-desktop"
            topline="Устройства"
            title="Активные сессии"
            text="Контролируйте устройства, на которых выполнен вход в аккаунт."
        >
            <SettingsSecuritySessions
                :sessions="sessions"
                :disabled="isSaving"
                @logout-all="logoutAllUserSessions"
                @logout-session="logoutUserSession"
            />
        </SettingsSectionCard>
        </template>
    </SettingsPageShell>
</template>
