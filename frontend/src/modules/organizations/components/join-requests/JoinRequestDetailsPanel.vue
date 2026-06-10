<script setup lang="ts">
import OrganizationStatusBadge from "../shared/OrganizationStatusBadge.vue";

import type { OrganizationDetailsView } from "../../types";

interface Props {
    details: OrganizationDetailsView | null;
    canReview?: boolean;
    approveLabel?: string;
    rejectLabel?: string;
    closeLabel?: string;
}

interface Emits {
    (event: "approve"): void;
    (event: "reject"): void;
    (event: "close"): void;
}

withDefaults(defineProps<Props>(), {
    canReview: false,
    approveLabel: "Принять",
    rejectLabel: "Отклонить",
    closeLabel: "Закрыть",
});

defineEmits<Emits>();
</script>

<template>
    <aside
        v-if="details"
        class="org-details"
    >
        <header class="org-details__header">
            <div class="org-details__top">
                <div class="org-details__identity">
                    <span class="org-details__icon">
                        {{ details.title.slice(0, 2).toUpperCase() }}
                    </span>

                    <div class="org-details__title-wrap">
                        <span class="org-details__eyebrow">
                            {{ details.eyebrow }}
                        </span>

                        <h2 class="org-details__title">
                            {{ details.title }}
                        </h2>

                        <p class="org-details__subtitle">
                            {{ details.subtitle }}
                        </p>
                    </div>
                </div>

                <div class="org-details__actions">
                    <button
                        v-if="canReview"
                        class="org-details__action"
                        type="button"
                        :title="approveLabel"
                        @click="$emit('approve')"
                    >
                        ✓
                    </button>

                    <button
                        v-if="canReview"
                        class="org-details__action org-details__action--danger"
                        type="button"
                        :title="rejectLabel"
                        @click="$emit('reject')"
                    >
                        ×
                    </button>

                    <button
                        class="org-details__action"
                        type="button"
                        :title="closeLabel"
                        @click="$emit('close')"
                    >
                        ↩
                    </button>
                </div>
            </div>

            <div class="org-details__meta">
                <OrganizationStatusBadge :status="details.status" />

                <span
                    v-for="chip in details.chips"
                    :key="chip"
                    class="org-details__chip"
                >
                    {{ chip }}
                </span>
            </div>
        </header>

        <div class="org-details__body">
            <section class="org-details__section">
                <h3 class="org-details__section-title">
                    Информация по заявке
                </h3>

                <ul class="org-details__list">
                    <li
                        v-for="row in details.rows"
                        :key="row.label"
                        class="org-details__item"
                    >
                        <span class="org-details__label">
                            {{ row.label }}
                        </span>

                        <a
                            v-if="row.href"
                            class="org-details__value org-details__link"
                            :href="row.href"
                            target="_blank"
                            rel="noreferrer"
                        >
                            {{ row.value }}
                        </a>

                        <span
                            v-else
                            class="org-details__value"
                        >
                            {{ row.value }}
                        </span>
                    </li>
                </ul>
            </section>

            <slot />
        </div>
    </aside>
</template>