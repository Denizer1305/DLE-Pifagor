<script setup lang="ts">
import type {
    ContactCtaContent,
    PublicContactAction,
} from "@/modules/public/types/contact.types";

interface Props {
    content: ContactCtaContent;
}

defineProps<Props>();

function getActionClass(action: PublicContactAction): string[] {
    return [
        "cta-btn",
        action.variant === "primary" ? "primary" : "secondary",
    ];
}
</script>

<template>
    <section class="section contact-page-cta">
        <div class="container">
            <div class="contact-page-cta-shell fade-in visible">
                <h2>
                    {{ content.title }}
                </h2>

                <p>
                    {{ content.text }}
                </p>

                <div class="contact-page-cta-actions">
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

                <div class="contact-page-cta-note">
                    {{ content.note }}
                </div>
            </div>
        </div>
    </section>
</template>
