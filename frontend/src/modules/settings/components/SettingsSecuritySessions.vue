<script setup lang="ts">
import type {
    SecuritySessionDto,
    SecuritySessionsDto,
} from "@/modules/settings/types/settings.types";

interface Props {
    sessions: SecuritySessionsDto | null;
    disabled?: boolean;
}

interface Emits {
    (event: "logout-all"): void;
    (event: "logout-session", sessionId: string): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

function getSessionIcon(session: SecuritySessionDto): string {
    if (session.device.toLowerCase().includes("mobile")) {
        return "fas fa-mobile-screen";
    }

    return "fas fa-desktop";
}
</script>

<template>
    <div class="security-sessions-card">
        <div class="security-sessions-head">
            <div>
                <h3>Активные сессии</h3>
                <p>
                    Устройства и браузеры, через которые выполнен вход в аккаунт.
                </p>
            </div>

            <button
                type="button"
                class="security-danger-btn"
                :disabled="disabled || !sessions?.can_logout_all"
                @click="emit('logout-all')"
            >
                <i class="fas fa-right-from-bracket"></i>
                Завершить все
            </button>
        </div>

        <div class="security-sessions-list">
            <div
                v-for="session in sessions?.items || []"
                :key="session.id"
                class="security-session-item"
            >
                <div class="security-session-icon">
                    <i :class="getSessionIcon(session)"></i>
                </div>

                <div class="security-session-copy">
                    <strong>{{ session.title }}</strong>
                    <span>{{ session.device }}</span>
                    <small>{{ session.ip_address }}</small>
                </div>

                <span
                    v-if="session.is_current"
                    class="security-session-current"
                >
                    Текущая
                </span>

                <button
                    v-else
                    type="button"
                    class="security-session-btn"
                    :disabled="disabled"
                    @click="emit('logout-session', session.id)"
                >
                    Завершить
                </button>
            </div>
        </div>
    </div>
</template>