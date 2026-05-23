<script setup lang="ts">
import { RouterLink } from "vue-router";

import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import {
    publicFooterGroups,
    publicSocialLinks,
} from "@/modules/public/data/public-navigation.data";
import { useThemedLogo } from "@/composables/useThemedLogo";

const currentYear = new Date().getFullYear();

const { logoSrc } = useThemedLogo();
const { localizePublicContent, t } = useI18n();

const footerLinks = computed(() => {
    return localizePublicContent(publicFooterGroups).flatMap((group) => group.links);
});

const socialLinks = computed(() => {
    return localizePublicContent(publicSocialLinks);
});
</script>

<template>
    <footer class="site-footer">
        <div class="container">
            <div class="footer-shell">
                <div class="footer-main">
                    <RouterLink
                        class="footer-brand"
                        :to="{ name: 'home' }"
                    >
                        <span class="footer-brand-mark">
                            <img
                                :src="logoSrc"
                                :alt="t('footer.brandName')"
                            />
                        </span>

                        <span class="footer-brand-copy">
                            <h3>{{ t("footer.brandName") }}</h3>

                            <p>
                                {{ t("footer.brandDescription") }}
                            </p>
                        </span>
                    </RouterLink>

                    <div class="footer-socials">
                        <a
                            v-for="social in socialLinks"
                            :key="social.label"
                            class="footer-social-link"
                            :href="social.href"
                        >
                            <i
                                class="base-icon"
                                :class="social.icon"
                            ></i>

                            {{ social.label }}
                        </a>
                    </div>
                </div>

                <div class="footer-bottom">
                    <nav
                        class="footer-nav"
                        :aria-label="t('footer.navigation')"
                    >
                        <RouterLink
                            v-for="link in footerLinks"
                            :key="`${link.routeName}-${link.label}`"
                            :to="{ name: link.routeName }"
                        >
                            {{ link.label }}
                        </RouterLink>
                    </nav>

                    <p class="footer-note">
                        {{ t("footer.note") }}
                    </p>
                </div>

                <div class="footer-legal">
                    <p>
                        © {{ currentYear }} {{ t("footer.brandName") }}. {{ t("footer.legal") }}
                    </p>
                </div>
            </div>
        </div>
    </footer>
</template>
