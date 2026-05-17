<script setup lang="ts">
import { RouterLink } from "vue-router";

import {
    publicFooterGroups,
    publicSocialLinks,
} from "@/modules/public/data/public-navigation.data";
import logoSrc from "@/assets/image/logo/logo.svg";

const currentYear = new Date().getFullYear();
</script>

<template>
    <footer class="public-footer">
        <div class="container public-footer__container">
            <div class="public-footer__main">
                <div class="public-footer__brand">
                    <RouterLink
                        class="public-footer__logo-link"
                        :to="{ name: 'home' }"
                    >
                        <img
                            class="public-footer__logo"
                            :src="logoSrc"
                            alt="ЦОС «Пифагор»"
                        />
                    </RouterLink>

                    <div>
                        <h2>ЦОС «Пифагор»</h2>

                        <p>
                            Цифровая образовательная среда для обучения,
                            наставничества, расписания, заданий и роста.
                        </p>
                    </div>
                </div>

                <div class="public-footer__groups">
                    <div
                        v-for="group in publicFooterGroups"
                        :key="group.title"
                        class="public-footer__group"
                    >
                        <h3>{{ group.title }}</h3>

                        <nav>
                            <RouterLink
                                v-for="link in group.links"
                                :key="link.routeName"
                                :to="{ name: link.routeName }"
                            >
                                {{ link.label }}
                            </RouterLink>
                        </nav>
                    </div>

                    <div class="public-footer__group">
                        <h3>Связь</h3>

                        <nav>
                            <a
                                v-for="social in publicSocialLinks"
                                :key="social.label"
                                :href="social.href"
                            >
                                <i :class="social.icon"></i>
                                {{ social.label }}
                            </a>
                        </nav>
                    </div>
                </div>
            </div>

            <div class="public-footer__bottom">
                <span>
                    © {{ currentYear }} ЦОС «Пифагор». Все права защищены.
                </span>

                <span>
                    Спокойное пространство для обучения, наставничества и развития.
                </span>
            </div>
        </div>
    </footer>
</template>