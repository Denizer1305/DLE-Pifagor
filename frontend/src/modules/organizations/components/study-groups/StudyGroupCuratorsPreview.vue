<script setup lang="ts">
import OrganizationStatusBadge from "../shared/OrganizationStatusBadge.vue";

import type { GroupCuratorListItemView } from "../../types";

interface Props {
    items: GroupCuratorListItemView[];
    title: string;
    emptyText: string;
    addLabel?: string;
    isAddVisible?: boolean;
}

interface Emits {
    (event: "select", item: GroupCuratorListItemView): void;
    (event: "add"): void;
}

withDefaults(defineProps<Props>(), {
    addLabel: "",
    isAddVisible: false,
});

defineEmits<Emits>();
</script>

<template>
    <section class="org-details__section">
        <div class="org-page__section-head">
            <div>
                <h3 class="org-details__section-title">
                    {{ title }}
                </h3>
            </div>

            <button
                v-if="isAddVisible && addLabel"
                class="org-form__button"
                type="button"
                @click="$emit('add')"
            >
                {{ addLabel }}
            </button>
        </div>

        <div
            v-if="items.length"
            class="org-request"
        >
            <article
                v-for="item in items"
                :key="item.id"
                class="org-request-card"
            >
                <header class="org-request-card__header">
                    <button
                        class="org-request-card__identity"
                        type="button"
                        @click="$emit('select', item)"
                    >
                        <span class="org-request-card__icon">
                            {{ item.teacherName.slice(0, 2).toUpperCase() }}
                        </span>

                        <span class="org-request-card__content">
                            <span class="org-request-card__title">
                                {{ item.teacherName }}
                            </span>

                            <span class="org-request-card__subtitle">
                                {{ item.teacherEmail }} · {{ item.teacherPhone }}
                            </span>
                        </span>
                    </button>

                    <OrganizationStatusBadge :status="item.status" />
                </header>

                <div class="org-request-card__meta">
                    <div class="org-request-card__meta-item">
                        <span class="org-request-card__meta-label">
                            Группа
                        </span>

                        <span class="org-request-card__meta-value">
                            {{ item.groupTitle }}
                        </span>
                    </div>

                    <div class="org-request-card__meta-item">
                        <span class="org-request-card__meta-label">
                            Роль
                        </span>

                        <span class="org-request-card__meta-value">
                            {{ item.isPrimary ? "Основной куратор" : "Дополнительный куратор" }}
                        </span>
                    </div>
                </div>
            </article>
        </div>

        <p
            v-else
            class="org-details__text"
        >
            {{ emptyText }}
        </p>
    </section>
</template>
