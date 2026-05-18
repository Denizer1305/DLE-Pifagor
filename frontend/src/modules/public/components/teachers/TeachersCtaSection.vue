<script setup lang="ts">
import type {
    PublicTeachersAction,
    TeachersCtaContent,
} from "@/modules/public/types/public-teachers.types";

interface Props {
    content: TeachersCtaContent;
}

defineProps<Props>();

function getActionClass(action: PublicTeachersAction): string[] {
    const variant = action.variant || "primary";

    return [
        "cta-btn",
        variant === "primary" ? "primary" : "secondary",
    ];
}
</script>

<template>
    <section class="section teachers-page-cta">
        <div class="container">
            <div class="teachers-page-cta-shell fade-in">
                <h2>
                    {{ content.title }}
                </h2>

                <p>
                    {{ content.text }}
                </p>

                <div class="teachers-page-cta-actions">
                    <component
                        :is="action.to ? 'RouterLink' : 'a'"
                        v-for="action in content.actions"
                        :key="action.label"
                        :to="action.to"
                        :href="action.href"
                        :class="getActionClass(action)"
                    >
                        {{ action.label }}

                        <i
                            v-if="action.icon"
                            :class="action.icon"
                        ></i>
                    </component>
                </div>

                <div class="teachers-page-cta-note">
                    {{ content.note }}
                </div>
            </div>
        </div>
    </section>
</template>
