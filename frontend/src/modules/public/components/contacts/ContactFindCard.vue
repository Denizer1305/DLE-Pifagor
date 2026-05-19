<script setup lang="ts">
import type { ContactFindContent } from "@/modules/public/types/contact.types";

interface Props {
    content: ContactFindContent;
}

defineProps<Props>();
</script>

<template>
    <div class="contact-card contact-find-card">
        <div class="contact-card-inner">
            <div class="contact-card-topline">
                <i :class="content.toplineIcon"></i>
                {{ content.topline }}
            </div>

            <h3 class="contact-card-title">
                {{ content.title }}
            </h3>

            <p class="contact-card-text">
                {{ content.text }}
            </p>

            <div class="contact-find-steps">
                <div
                    v-for="step in content.steps"
                    :key="step.number"
                    class="contact-find-step"
                >
                    <div class="contact-find-step-number">
                        {{ step.number }}
                    </div>

                    <div>
                        <strong>{{ step.title }}</strong>
                        <span>{{ step.text }}</span>
                    </div>
                </div>
            </div>

            <ul class="contact-note-list">
                <li
                    v-for="note in content.notes"
                    :key="note"
                >
                    <i class="fas fa-check-circle"></i>
                    <span>{{ note }}</span>
                </li>
            </ul>
        </div>
    </div>
</template>
