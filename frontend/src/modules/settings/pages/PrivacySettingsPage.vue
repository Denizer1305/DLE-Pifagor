<script setup lang="ts">
import SettingsPageShell from "@/modules/settings/components/SettingsPageShell.vue";
import SettingsPrivacyMatrix from "@/modules/settings/components/SettingsPrivacyMatrix.vue";
import SettingsSectionCard from "@/modules/settings/components/SettingsSectionCard.vue";
import SettingsSelectRow from "@/modules/settings/components/SettingsSelectRow.vue";
import SettingsToggleRow from "@/modules/settings/components/SettingsToggleRow.vue";

import { profileVisibilityOptions } from "@/modules/settings/data/settings-options.data";
import { usePrivacySettings } from "@/modules/settings/composables/usePrivacySettings";

import type {
    PrivacySettingsDto,
    ProfileVisibility,
} from "@/modules/settings/types/settings.types";

const {
    settings,
    pageState,
    isLoading,
    isSaving,
    errorMessage,
    loadPrivacySettings,
    updatePrivacy,
} = usePrivacySettings();

async function updateVisibility(value: string): Promise<void> {
    await updatePrivacy({
        profile_visibility: value as ProfileVisibility,
    });
}

async function updateMatrix(value: Partial<PrivacySettingsDto>): Promise<void> {
    await updatePrivacy(value);
}

</script>

<template>
    <SettingsPageShell
        :model="pageState?.scaffold"
        :hero="pageState?.hero"
        :is-ready="Boolean(pageState && settings)"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем настройки приватности..."
        @reload="loadPrivacySettings"
    >
        <template v-if="settings">
        <SettingsSectionCard
            icon="fas fa-user-circle"
            topline="Видимость профиля"
            title="Кто может видеть ваш профиль"
            text="Определите общий уровень доступности профиля внутри образовательной платформы."
        >
            <SettingsSelectRow
                label="Уровень видимости профиля"
                text="Эта настройка задаёт базовое правило доступа к профилю."
                :model-value="settings.profile_visibility"
                :options="profileVisibilityOptions"
                :disabled="isSaving"
                @update:model-value="updateVisibility"
            />
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-eye"
            topline="Поля профиля"
            title="Какие данные можно показывать"
            text="Настройте видимость отдельных полей профиля и разрешения для разных групп пользователей."
        >
            <SettingsPrivacyMatrix
                :settings="settings"
                :disabled="isSaving"
                @update="updateMatrix"
            />
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-file-export"
            topline="Персональные данные"
            title="Экспорт и обработка данных"
            text="Экспорт персональных данных будет реализован отдельным этапом, но настройка доступа уже сохраняется."
        >
            <div class="settings-toggle-list">
                <SettingsToggleRow
                    label="Разрешить экспорт персональных данных"
                    text="Позже пользователь сможет скачать копию своих данных из платформы."
                    :model-value="settings.allow_data_export"
                    :disabled="isSaving"
                    @update:model-value="updatePrivacy({ allow_data_export: $event })"
                />
            </div>

            <div class="settings-info-card">
                <div class="settings-info-card-icon">
                    <i class="fas fa-circle-info"></i>
                </div>

                <div class="settings-info-card-copy">
                    <strong>Экспорт будет подключён позже</strong>
                    <span>
                        Сейчас настройка сохраняется в backend и будет использована при реализации выгрузки данных.
                    </span>
                </div>
            </div>
        </SettingsSectionCard>
        </template>
    </SettingsPageShell>
</template>
