<script setup lang="ts">
interface Props {
    unreadCount: number;
    isLoading?: boolean;
    disabled?: boolean;
}

interface Emits {
    (event: "read-all"): void;
    (event: "reload"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="notification-page-header fade-in visible">
        <div class="notification-page-header__bg" aria-hidden="true">
            <div class="notification-page-header__circle one"></div>
            <div class="notification-page-header__circle two"></div>
        </div>

        <div class="notification-page-header__content">
            <div class="notification-page-header__topline">
                <i class="fas fa-bell"></i>
                Центр уведомлений
            </div>

            <h1>Все важные события платформы в одном месте</h1>

            <p>
                Здесь отображаются ежедневные сводки, дедлайны, напоминания,
                системные сообщения, поздравления и события, требующие внимания.
            </p>

            <div class="notification-page-header__stats">
                <span>
                    <strong>{{ unreadCount }}</strong>
                    непрочитанных
                </span>

                <span>
                    <strong>7</strong>
                    дней хранения после выполнения
                </span>
            </div>
        </div>

        <div class="notification-page-header__actions">
            <button
                type="button"
                :disabled="disabled || unreadCount === 0"
                @click="emit('read-all')"
            >
                <i class="fas fa-check-double"></i>
                Прочитать все
            </button>

            <button
                type="button"
                :disabled="isLoading"
                @click="emit('reload')"
            >
                <i class="fas fa-rotate-right"></i>
                Обновить
            </button>
        </div>
    </section>
</template>