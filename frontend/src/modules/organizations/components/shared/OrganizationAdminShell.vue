<script setup lang="ts">
import OrganizationEntityTabs from "./OrganizationEntityTabs.vue";
import OrganizationPageHeader from "./OrganizationPageHeader.vue";

import type {
    OrganizationEntityKey,
    OrganizationNavigationItem,
    OrganizationPageHeaderView,
    OrganizationSummaryCardView,
} from "../../types";

interface Props {
    rootHeader: OrganizationPageHeaderView;
    pageHeader: OrganizationPageHeaderView;
    navigation: OrganizationNavigationItem[];
    activeEntity: OrganizationEntityKey;
    summary?: OrganizationSummaryCardView[];
}

interface Emits {
    (event: "select-entity", key: OrganizationEntityKey): void;
    (event: "primary-action"): void;
    (event: "secondary-action"): void;
}

withDefaults(defineProps<Props>(), {
    summary: () => [],
});

defineEmits<Emits>();
</script>

<template>
    <section class="org-admin">
        <div class="org-admin__shell">
            <div class="org-admin__surface">
                <div class="org-admin__inner">
                    <OrganizationPageHeader
                        :header="rootHeader"
                        :is-primary-action-visible="false"
                    >
                        <template
                            v-if="$slots.rootActions"
                            #actions
                        >
                            <slot name="rootActions" />
                        </template>
                    </OrganizationPageHeader>

                    <div
                        v-if="summary.length || $slots.summary"
                        class="org-summary"
                    >
                        <slot name="summary">
                            <div class="org-summary__grid">
                                <article
                                    v-for="card in summary"
                                    :key="card.key"
                                    class="org-summary-card"
                                    :class="`org-summary-card--${card.tone}`"
                                >
                                    <div class="org-summary-card__top">
                                        <span class="org-summary-card__icon">
                                            <slot
                                                name="summary-icon"
                                                :icon="card.icon"
                                                :card="card"
                                            >
                                                {{ card.icon }}
                                            </slot>
                                        </span>

                                        <span
                                            v-if="card.trend"
                                            class="org-summary-card__trend"
                                            :class="`is-${card.trend.tone}`"
                                        >
                                            {{ card.trend.label }}
                                        </span>
                                    </div>

                                    <div>
                                        <span class="org-summary-card__label">
                                            {{ card.label }}
                                        </span>

                                        <strong class="org-summary-card__value">
                                            {{ card.value }}
                                        </strong>
                                    </div>

                                    <p class="org-summary-card__meta">
                                        {{ card.meta }}
                                    </p>
                                </article>
                            </div>
                        </slot>
                    </div>
                </div>
            </div>

            <div class="org-admin__layout">
                <aside class="org-admin__sidebar">
                    <OrganizationEntityTabs
                        :items="navigation"
                        :active-key="activeEntity"
                        @select="$emit('select-entity', $event)"
                    >
                        <template
                            v-if="$slots.navigationIcon"
                            #icon="{ icon, item }"
                        >
                            <slot
                                name="navigationIcon"
                                :icon="icon"
                                :item="item"
                            />
                        </template>
                    </OrganizationEntityTabs>
                </aside>

                <main class="org-admin__content">
                    <section class="org-page">
                        <OrganizationPageHeader
                            :header="pageHeader"
                            @primary-action="$emit('primary-action')"
                            @secondary-action="$emit('secondary-action')"
                        >
                            <template
                                v-if="$slots.pageActions"
                                #actions
                            >
                                <slot name="pageActions" />
                            </template>
                        </OrganizationPageHeader>

                        <div class="org-page__body">
                            <slot />
                        </div>
                    </section>
                </main>
            </div>
        </div>
    </section>
</template>