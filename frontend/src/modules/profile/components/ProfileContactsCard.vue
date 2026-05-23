<script setup lang="ts">
import type {
    ProfileContactItemModel,
    ProfileContactsCardModel,
} from "@/modules/profile/types/profile.types";

interface Props {
    card: ProfileContactsCardModel;
}

defineProps<Props>();

function getExternalTarget(contact: ProfileContactItemModel): string | undefined {
    if (!contact.href || contact.key === "email" || contact.key === "phone") {
        return undefined;
    }

    return "_blank";
}

function getExternalRel(contact: ProfileContactItemModel): string | undefined {
    if (!contact.href || contact.key === "email" || contact.key === "phone") {
        return undefined;
    }

    return "noopener noreferrer";
}
</script>

<template>
    <section class="profile-communication-hub fade-in visible">
        <div class="profile-communication-grid">
            <article class="profile-communication-card">
                <div class="profile-communication-head">
                    <div class="profile-communication-topline">
                        <i class="fas fa-paper-plane"></i>
                        Контакты и соцсети
                    </div>

                    <h2 class="profile-communication-title">
                        {{ card.title }}
                    </h2>

                    <p class="profile-communication-text">
                        {{ card.text }}
                    </p>
                </div>

                <div class="profile-communication-list">
                    <a
                        v-for="contact in card.contacts"
                        :key="contact.key"
                        class="profile-communication-item"
                        :href="contact.href || '#'"
                        :target="getExternalTarget(contact)"
                        :rel="getExternalRel(contact)"
                    >
                        <span class="profile-communication-icon">
                            <i :class="contact.icon"></i>
                        </span>

                        <span class="profile-communication-body">
                            <span class="profile-communication-label">
                                {{ contact.label }}
                            </span>

                            <strong class="profile-communication-value">
                                {{ contact.value }}
                            </strong>
                        </span>

                        <span
                            v-if="contact.href"
                            class="profile-communication-arrow"
                        >
                            <i class="fas fa-arrow-up-right-from-square"></i>
                        </span>
                    </a>
                </div>
            </article>

            <aside class="profile-communication-side">
                <div class="profile-communication-note">
                    <div class="profile-communication-note-topline">
                        <i class="fas fa-circle-info"></i>
                        Небольшая заметка
                    </div>

                    <h3 class="profile-communication-note-title">
                        Публичные и рабочие контакты
                    </h3>

                    <p class="profile-communication-note-text">
                        В этом блоке показываются только актуальные каналы связи,
                        которые используются для уведомлений, учебных вопросов
                        и профессионального общения.
                    </p>
                </div>

                <div
                    v-if="card.statuses.length"
                    class="profile-communication-status"
                >
                    <div
                        v-for="status in card.statuses"
                        :key="status.label"
                        class="profile-communication-status-row"
                    >
                        <span>{{ status.label }}</span>
                        <strong>{{ status.value }}</strong>
                    </div>
                </div>
            </aside>
        </div>
    </section>
</template>