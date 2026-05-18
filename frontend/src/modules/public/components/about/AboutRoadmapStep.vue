<script setup lang="ts">
import type { AboutRoadmapStepContent } from "@/modules/public/data/about-page.data";

interface Props {
    step: AboutRoadmapStepContent;
}

defineProps<Props>();
</script>

<template>
    <div class="about-roadmap-step fade-in">
        <div class="about-roadmap-card">
            <h3>
                {{ step.title }}
            </h3>

            <p>
                {{ step.text }}
            </p>

            <ul>
                <li
                    v-for="point in step.points"
                    :key="point"
                >
                    <i class="base-icon fas fa-check-circle"></i>
                    <span>{{ point }}</span>
                </li>
            </ul>
        </div>
    </div>
</template>
