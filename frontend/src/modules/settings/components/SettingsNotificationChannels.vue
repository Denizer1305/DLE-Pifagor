<script setup lang="ts">
import SettingsToggleRow from "@/modules/settings/components/SettingsToggleRow.vue";
import type { NotificationSettingsDto } from "@/modules/settings/types/settings.types";

interface Props {
    channels: NotificationSettingsDto["channels"];
    disabled?: boolean;
}

interface Emits {
    (event: "update", value: Partial<NotificationSettingsDto["channels"]>): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

function updateChannel(
    key: keyof NotificationSettingsDto["channels"],
    value: boolean,
): void {
    emit("update", {
        [key]: value,
    });
}
</script>

<template>
    <div class="notifications-channel-grid">
        <SettingsToggleRow
            label="Внутри платформы"
            text="Уведомления в верхней панели и центре событий."
            :model-value="channels.in_app"
            :disabled="disabled"
            @update:model-value="updateChannel('in_app', $event)"
        />

        <SettingsToggleRow
            label="Email"
            text="Письма о важных событиях, безопасности и дайджестах."
            :model-value="channels.email"
            :disabled="disabled"
            @update:model-value="updateChannel('email', $event)"
        />

        <SettingsToggleRow
            label="VK"
            text="Получение уведомлений через подключённый VK-аккаунт."
            :model-value="channels.vk"
            :disabled="disabled"
            @update:model-value="updateChannel('vk', $event)"
        />

        <SettingsToggleRow
            label="MAX"
            text="Получение важных сообщений через MAX после подключения."
            :model-value="channels.max"
            :disabled="disabled"
            @update:model-value="updateChannel('max', $event)"
        />
    </div>
</template>