<script setup lang="ts">
import { ref } from "vue";

import { useThemedLogo } from "@/composables/useThemedLogo";
import { useFloatingCanvas } from "@/modules/public/composables/useFloatingCanvas";
import type { HomeHeroContent, PublicAction } from "@/modules/public/data/home-page.data";

interface Props {
    content: HomeHeroContent;
}

defineProps<Props>();

const heroCanvasRef = ref<HTMLCanvasElement | null>(null);

const heroCircles = ["one", "two", "three"];
const heroGlows = ["one", "two"];
const movingLines = ["one", "two", "three"];
const diagonalLines = ["one", "two", "three"];
const floatingDots = ["one", "two", "three", "four"];
const rings = ["one", "two", "three"];
const { heroLogoSrc } = useThemedLogo();

useFloatingCanvas(heroCanvasRef, {
    pointsCount: 42,
    mobilePointsCount: 24,
    lineDistance: 90,
    wavesEnabled: true,
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
    <section class="hero">
        <div
            class="hero-grid-lines"
            aria-hidden="true"
        >
            <div class="hero-grid-line vertical left"></div>
            <div class="hero-grid-line vertical center"></div>
            <div class="hero-grid-line vertical right"></div>
            <div class="hero-grid-line horizontal top"></div>
            <div class="hero-grid-line horizontal bottom"></div>
        </div>

        <canvas
            ref="heroCanvasRef"
            class="hero-canvas"
            aria-hidden="true"
        ></canvas>

        <div
            class="hero-decor"
            aria-hidden="true"
        >
            <div
                v-for="circle in heroCircles"
                :key="`circle-${circle}`"
                class="hero-circle"
                :class="circle"
            ></div>

            <div
                v-for="glow in heroGlows"
                :key="`glow-${glow}`"
                class="hero-glow"
                :class="glow"
            ></div>

            <div
                v-for="line in movingLines"
                :key="`moving-line-${line}`"
                class="hero-moving-line"
                :class="line"
            ></div>

            <div
                v-for="diagonal in diagonalLines"
                :key="`diagonal-${diagonal}`"
                class="hero-diagonal"
                :class="diagonal"
            ></div>

            <div
                v-for="dot in floatingDots"
                :key="`floating-dot-${dot}`"
                class="hero-floating-dot"
                :class="dot"
            ></div>
        </div>

        <div class="container hero-container">
            <div class="hero-content">
                <div class="hero-top-badges fade-in">
                    <span
                        v-for="badge in content.badges"
                        :key="badge.text"
                        class="hero-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.text }}
                    </span>
                </div>

                <h1 class="hero-title fade-in">
                    {{ content.title }}
                </h1>

                <p class="hero-subtitle fade-in">
                    {{ content.subtitle }}
                </p>

                <p class="hero-description fade-in">
                    {{ content.description }}
                </p>

                <div class="hero-highlight fade-in">
                    <div
                        v-for="highlight in content.highlights"
                        :key="highlight"
                        class="hero-highlight-item"
                    >
                        <i class="fas fa-circle"></i>
                        <span>{{ highlight }}</span>
                    </div>
                </div>

                <div class="hero-actions">
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
                        :key="`ring-${ring}`"
                        class="hero-ring"
                        :class="ring"
                    ></div>

                    <div class="hero-dot one"></div>
                    <div class="hero-dot two"></div>

                    <div class="hero-mini-line one"></div>
                    <div class="hero-mini-line two"></div>

                    <div class="hero-greek-mark one">
                        Π
                    </div>

                    <div class="hero-greek-mark two">
                        Δ
                    </div>

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
