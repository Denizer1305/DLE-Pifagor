<script setup lang="ts">
import heroLogo from "@/assets/brand/logo/themes/light/hero-logo.svg";
import { useI18n } from "@/composables/useI18n";
import { useThemedLogo } from "@/composables/useThemedLogo";
import type { AuthIntroConfig } from "@/modules/auth/types/auth-form.types";

interface Props {
    intro: AuthIntroConfig;
    logoSrc?: string;
}

const props = withDefaults(defineProps<Props>(), {
    logoSrc: heroLogo,
});

const { getThemedLogoSrc } = useThemedLogo();
const { tr } = useI18n();
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
                            :src="getThemedLogoSrc(props.logoSrc)"
                            :alt="tr('Пифагор — цифровая образовательная среда')"
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
                    {{ tr(badge.label) }}
                </span>
            </div>

            <h1 class="auth-title">
                {{ tr(intro.title) }}
            </h1>

            <p class="auth-subtitle">
                {{ tr(intro.subtitle) }}
            </p>

            <div class="auth-meta">
                <div
                    v-for="item in intro.meta"
                    :key="item.label"
                    class="auth-meta-item"
                >
                    <i :class="item.icon"></i>
                    {{ tr(item.label) }}
                </div>
            </div>
        </div>
    </section>
</template>
