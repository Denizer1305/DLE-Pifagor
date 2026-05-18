<script setup lang="ts">
import { RouterLink } from "vue-router";

import {
    publicFooterGroups,
    publicSocialLinks,
} from "@/modules/public/data/public-navigation.data";
import logoSrc from "@/assets/image/logo/logo.svg";

const currentYear = new Date().getFullYear();

const footerLinks = publicFooterGroups.flatMap((group) => group.links);
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
                                alt="ЦОС «Пифагор»"
                            />
                        </span>

                        <span class="footer-brand-copy">
                            <h3>ЦОС «Пифагор»</h3>

                            <p>
                                Цифровая образовательная среда для обучения,
                                наставничества, расписания, заданий и роста.
                            </p>
                        </span>
                    </RouterLink>

                    <div class="footer-socials">
                        <a
                            v-for="social in publicSocialLinks"
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
                        aria-label="Навигация в подвале"
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
                        Спокойное пространство для обучения, наставничества и развития.
                    </p>
                </div>

                <div class="footer-legal">
                    <p>
                        © {{ currentYear }} ЦОС «Пифагор». Все права защищены.
                    </p>
                </div>
            </div>
        </div>
    </footer>
</template>
