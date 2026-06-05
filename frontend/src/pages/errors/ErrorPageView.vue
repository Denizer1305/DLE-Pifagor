<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";

import { useI18n } from "@/composables/useI18n";

import ErrorActions from "./components/ErrorActions.vue";
import ErrorAnimatedBackdrop from "./components/ErrorAnimatedBackdrop.vue";
import ErrorDetailsCard from "./components/ErrorDetailsCard.vue";
import ErrorFooter from "./components/ErrorFooter.vue";
import ErrorNotes from "./components/ErrorNotes.vue";
import ErrorQuickLinks from "./components/ErrorQuickLinks.vue";
import ErrorThemeToggle from "./components/ErrorThemeToggle.vue";
import ErrorVisual from "./components/ErrorVisual.vue";
import type { ErrorPageAction, ErrorPageContent } from "./error-pages.data";

const props = defineProps<{
    content: ErrorPageContent;
}>();

const router = useRouter();
const { tr } = useI18n();

const localizedContent = computed<ErrorPageContent>(() => {
    return {
        ...props.content,
        title: tr(props.content.title),
        subtitle: tr(props.content.subtitle),
        description: tr(props.content.description),
        details: props.content.details
            ? {
                ...props.content.details,
                title: tr(props.content.details.title),
                items: props.content.details.items.map((item) => tr(item)),
            }
            : undefined,
        quickLinks: props.content.quickLinks?.map((link) => ({
            ...link,
            title: tr(link.title),
            description: tr(link.description),
        })),
        notes: props.content.notes.map((note) => ({
            ...note,
            text: tr(note.text),
        })),
        actions: props.content.actions.map((action) => ({
            ...action,
            label: tr(action.label),
        })),
        footer: {
            ...props.content.footer,
            text: tr(props.content.footer.text),
        },
    };
});

function handleAction(action: ErrorPageAction): void {
    if (action.action !== "back") {
        return;
    }

    if (window.history.length > 1) {
        router.back();
        return;
    }

    router.push({ name: "home" });
}
</script>

<template>
    <main :class="['error-page', `error-page--${content.variant}`]">
        <ErrorAnimatedBackdrop :variant="content.variant" />
        <ErrorThemeToggle />

        <section
            class="error-hero"
            :aria-labelledby="`error-title-${content.code}`"
        >
            <div class="error-content">
                <p class="error-code">
                    {{ content.code }}
                </p>

                <h1
                    :id="`error-title-${content.code}`"
                    class="error-title"
                >
                    {{ localizedContent.title }}
                </h1>

                <p class="error-subtitle">
                    {{ localizedContent.subtitle }}
                </p>

                <p class="error-description">
                    {{ localizedContent.description }}
                </p>

                <ErrorDetailsCard
                    v-if="localizedContent.details"
                    :details="localizedContent.details"
                />

                <ErrorQuickLinks
                    v-if="localizedContent.quickLinks?.length"
                    :links="localizedContent.quickLinks"
                />

                <ErrorActions
                    :actions="localizedContent.actions"
                    @action="handleAction"
                />

                <ErrorNotes :notes="localizedContent.notes" />
            </div>

            <ErrorVisual
                :visual-icon="content.visualIcon"
                :orbit-icon="content.orbitIcon"
            />
        </section>

        <ErrorFooter
            :text="localizedContent.footer.text"
            :address="localizedContent.footer.address"
            :email="localizedContent.footer.email"
            :phone="localizedContent.footer.phone"
        />
    </main>
</template>
