<script setup lang="ts">
import SettingsNotificationChannels from "@/modules/settings/components/SettingsNotificationChannels.vue";
import SettingsPageShell from "@/modules/settings/components/SettingsPageShell.vue";
import SettingsSectionCard from "@/modules/settings/components/SettingsSectionCard.vue";
import SettingsSelectRow from "@/modules/settings/components/SettingsSelectRow.vue";

import { notificationFrequencyOptions } from "@/modules/settings/data/settings-options.data";
import { useNotificationSettings } from "@/modules/settings/composables/useNotificationSettings";

import type {
    NotificationFrequency,
    NotificationSettingsDto,
} from "@/modules/settings/types/settings.types";

const {
    settings,
    pageState,
    isLoading,
    isSaving,
    errorMessage,
    loadNotificationSettings,
    updateNotifications,
} = useNotificationSettings();

async function updateChannels(
    value: Partial<NotificationSettingsDto["channels"]>,
): Promise<void> {
    if (!settings.value) {
        return;
    }

    await updateNotifications({
        channels: {
            ...settings.value.channels,
            ...value,
        },
    });
}

async function updateFrequency(
    key: keyof NotificationSettingsDto["frequency"],
    value: string,
): Promise<void> {
    if (!settings.value) {
        return;
    }

    await updateNotifications({
        frequency: {
            ...settings.value.frequency,
            [key]: value as NotificationFrequency,
        },
    });
}

async function updateDigestTime(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;

    await updateNotifications({
        digest_time: input.value,
    });
}

</script>

<template>
    <SettingsPageShell
        :model="pageState?.scaffold"
        :hero="pageState?.hero"
        :is-ready="Boolean(pageState && settings)"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем настройки уведомлений..."
        @reload="loadNotificationSettings"
    >
        <template v-if="settings">
        <SettingsSectionCard
            icon="fas fa-bell"
            topline="Каналы доставки"
            title="Куда отправлять уведомления"
            text="Выберите каналы, через которые платформа будет отправлять важные события, напоминания и дайджесты."
        >
            <SettingsNotificationChannels
                :channels="settings.channels"
                :disabled="isSaving"
                @update="updateChannels"
            />
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-clock"
            topline="Частота уведомлений"
            title="Когда отправлять события"
            text="Для каждой категории можно выбрать отдельную частоту: сразу, ежедневно, еженедельно или отключить."
        >
            <div class="settings-form-grid">
                <SettingsSelectRow
                    label="Безопасность"
                    text="Входы в аккаунт, подозрительная активность и важные изменения защиты."
                    :model-value="settings.frequency.security"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('security', $event)"
                />

                <SettingsSelectRow
                    label="Учебные события"
                    text="Новые уроки, курсы, материалы и важные образовательные события."
                    :model-value="settings.frequency.education"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('education', $event)"
                />

                <SettingsSelectRow
                    label="Задания"
                    text="Домашние работы, практические задания, тесты и проверки."
                    :model-value="settings.frequency.assignments"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('assignments', $event)"
                />

                <SettingsSelectRow
                    label="Расписание"
                    text="Изменения занятий, консультаций, дедлайнов и календарных событий."
                    :model-value="settings.frequency.schedule"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('schedule', $event)"
                />

                <SettingsSelectRow
                    label="Обращения в поддержку"
                    text="Ответы поддержки, изменения статусов заявок и системные комментарии."
                    :model-value="settings.frequency.feedback"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('feedback', $event)"
                />

                <SettingsSelectRow
                    label="Системные события"
                    text="Технические уведомления, обновления платформы и административные сообщения."
                    :model-value="settings.frequency.system"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('system', $event)"
                />

                <SettingsSelectRow
                    label="Дайджест"
                    text="Сводка важных событий за день или неделю."
                    :model-value="settings.frequency.digest"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('digest', $event)"
                />

                <SettingsSelectRow
                    label="Информационные сообщения"
                    text="Новости платформы, рекомендации и необязательные сообщения."
                    :model-value="settings.frequency.marketing"
                    :options="notificationFrequencyOptions"
                    :disabled="isSaving"
                    @update:model-value="updateFrequency('marketing', $event)"
                />
            </div>
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-calendar-day"
            topline="Дайджест"
            title="Время ежедневной сводки"
            text="Выберите удобное время, когда платформа будет собирать и отправлять ежедневную сводку событий."
        >
            <div class="settings-form-grid">
                <label class="settings-select-row">
                    <span class="settings-select-copy">
                        <strong>Время дайджеста</strong>
                        <span>Например, 08:00 перед началом учебного дня.</span>
                    </span>

                    <input
                        class="settings-time-input"
                        type="time"
                        :value="settings.digest_time"
                        :disabled="isSaving"
                        @change="updateDigestTime"
                    />
                </label>
            </div>
        </SettingsSectionCard>
        </template>
    </SettingsPageShell>
</template>
