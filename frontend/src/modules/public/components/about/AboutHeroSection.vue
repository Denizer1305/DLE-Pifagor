<script setup lang="ts">
import { ref } from "vue";

import { useThemedLogo } from "@/composables/useThemedLogo";
import { useFloatingCanvas } from "@/modules/public/composables/useFloatingCanvas";
import type { AboutHeroContent, PublicAction } from "@/modules/public/data/about-page.data";

interface Props {
    content: AboutHeroContent;
}

defineProps<Props>();

const aboutHeroCanvasRef = ref<HTMLCanvasElement | null>(null);

const gridLines = [
    "vertical left",
    "vertical center",
    "vertical right",
    "horizontal top",
    "horizontal bottom",
];

const circles = ["one", "two", "three", "four", "five"];
const glows = ["one", "two", "three"];
const movingLines = ["one", "two", "three", "four"];
const floatingDots = ["one", "two", "three", "four"];
const rings = ["one", "two", "three"];
const { heroLogoSrc } = useThemedLogo();

useFloatingCanvas(aboutHeroCanvasRef, {
    pointsCount: 48,
    lineDistance: 135,
});

function getActionClass(action: PublicAction): string[] {
    const variant = action.variant || "primary";

    return [
        "btn",
        variant === "primary" ? "btn-primary" : "btn-light",
        "fade-in",
    ];
}
</script>

<template>
    <section class="about-hero">
        <div
            class="about-hero-grid-lines"
            aria-hidden="true"
        >
            <div
                v-for="line in gridLines"
                :key="line"
                class="about-hero-grid-line"
                :class="line"
            ></div>
        </div>

        <canvas
            ref="aboutHeroCanvasRef"
            class="about-hero-canvas"
            aria-hidden="true"
        ></canvas>

        <div
            class="about-hero-decor"
            aria-hidden="true"
        >
            <div
                v-for="circle in circles"
                :key="`circle-${circle}`"
                class="about-hero-circle"
                :class="circle"
            ></div>

            <div
                v-for="glow in glows"
                :key="`glow-${glow}`"
                class="about-hero-glow"
                :class="glow"
            ></div>

            <div
                v-for="line in movingLines"
                :key="`line-${line}`"
                class="about-hero-moving-line"
                :class="line"
            ></div>

            <div
                v-for="dot in floatingDots"
                :key="`dot-${dot}`"
                class="about-hero-floating-dot"
                :class="dot"
            ></div>
        </div>

        <div class="container about-hero-container">
            <div class="about-hero-content">
                <div class="about-hero-top-badges fade-in">
                    <span
                        v-for="badge in content.badges"
                        :key="badge.text"
                        class="about-hero-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.text }}
                    </span>
                </div>

                <h1 class="about-hero-title fade-in">
                    {{ content.title }}
                </h1>

                <p class="about-hero-subtitle fade-in">
                    {{ content.subtitle }}
                </p>

                <p class="about-hero-description fade-in">
                    {{ content.description }}
                </p>

                <div class="about-hero-highlight fade-in">
                    <div
                        v-for="highlight in content.highlights"
                        :key="highlight"
                        class="about-hero-highlight-item"
                    >
                        <i class="fas fa-circle"></i>
                        <span>{{ highlight }}</span>
                    </div>
                </div>

                <div class="about-hero-actions">
                    <RouterLink
                        v-for="action in content.actions"
                        :key="action.label"
                        :to="action.to"
                        :class="getActionClass(action)"
                    >
                        {{ action.label }}

                        <i
                            v-if="action.icon"
                            :class="action.icon"
                        ></i>
                    </RouterLink>
                </div>
            </div>

            <div class="hero-visual fade-in">
                <div class="hero-visual-shell">
                    <div
                        v-for="ring in rings"
                        :key="ring"
                        class="hero-ring"
                        :class="ring"
                    ></div>

                    <div class="hero-dot one"></div>
                    <div class="hero-dot two"></div>

                    <div class="hero-mini-line one"></div>
                    <div class="hero-mini-line two"></div>

                    <div class="hero-greek-mark one">Π</div>
                    <div class="hero-greek-mark two">Δ</div>

                    <div class="hero-logo-wrap">
                        <img
                            :src="heroLogoSrc"
                            :alt="content.logo.alt"
                        />
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
