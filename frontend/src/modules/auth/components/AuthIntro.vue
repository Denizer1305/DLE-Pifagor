<script setup lang="ts">
import heroLogo from "@/assets/image/logo/hero-logo.svg";
import type { AuthIntroConfig } from "@/modules/auth/types/auth-form.types";

interface Props {
    intro: AuthIntroConfig;
    logoSrc?: string;
}

withDefaults(defineProps<Props>(), {
    logoSrc: heroLogo,
});
</script>

<template>
    <section class="auth-intro fade-in">
        <div class="auth-intro-inner">
            <div class="auth-visual">
                <div class="auth-visual-shell">
                    <div class="auth-ring one"></div>
                    <div class="auth-ring two"></div>
                    <div class="auth-ring three"></div>

                    <div class="auth-dot one"></div>
                    <div class="auth-dot two"></div>

                    <div class="auth-mini-line one"></div>
                    <div class="auth-mini-line two"></div>

                    <div class="auth-mark one">Π</div>
                    <div class="auth-mark two">Δ</div>

                    <div class="auth-logo-wrap">
                        <img
                            :src="logoSrc"
                            alt="Пифагор — цифровая образовательная среда"
                        />
                    </div>
                </div>
            </div>

            <div class="auth-badges">
                <span
                    v-for="badge in intro.badges"
                    :key="badge.label"
                    class="auth-badge"
                >
                    <i :class="badge.icon"></i>
                    {{ badge.label }}
                </span>
            </div>

            <h1 class="auth-title">
                {{ intro.title }}
            </h1>

            <p class="auth-subtitle">
                {{ intro.subtitle }}
            </p>

            <div class="auth-meta">
                <div
                    v-for="item in intro.meta"
                    :key="item.label"
                    class="auth-meta-item"
                >
                    <i :class="item.icon"></i>
                    {{ item.label }}
                </div>
            </div>
        </div>
    </section>
</template>