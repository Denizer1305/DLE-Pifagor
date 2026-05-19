<script setup lang="ts">
import type { ContactSocialCardContent } from "@/modules/public/types/contact.types";

interface Props {
    content: ContactSocialCardContent;
}

defineProps<Props>();
</script>

<template>
    <div class="contact-card">
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

            <div class="contact-social-grid">
                <a
                    v-for="item in content.items"
                    :key="item.title"
                    :href="item.href"
                    class="contact-social-card"
                >
                    <i
                        v-if="item.icon"
                        :class="item.icon"
                    ></i>

                    <img
                        v-else-if="item.image"
                        :src="item.image"
                        alt=""
                        aria-hidden="true"
                    />

                    <strong>{{ item.title }}</strong>
                    <span>{{ item.text }}</span>
                </a>
            </div>
        </div>
    </div>
</template>
