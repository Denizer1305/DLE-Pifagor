<script setup lang="ts">
interface Props {
    title?: string;
    text?: string;
    icon?: string;
}

withDefaults(defineProps<Props>(), {
    title: "Уведомлений пока нет",
    text: "Когда появятся важные события, дедлайны, напоминания или системные сообщения, они будут отображаться здесь.",
    icon: "fas fa-bell-slash",
});
</script>

<template>
    <div class="notification-empty-state">
        <div class="notification-empty-state__icon">
            <i :class="icon"></i>
        </div>

        <div class="notification-empty-state__content">
            <strong>{{ title }}</strong>
            <p>{{ text }}</p>
        </div>
    </div>
</template>