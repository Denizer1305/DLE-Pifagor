<script setup lang="ts">
import { useThemedLogo } from "@/composables/useThemedLogo";
import { useI18n } from "@/composables/useI18n";
import type { ContactMapContent } from "@/modules/public/types/contact.types";

interface Props {
    content: ContactMapContent;
}

defineProps<Props>();

const { heroLogoSrc } = useThemedLogo();
const { t } = useI18n();
</script>

<template>
    <div
        id="contact-map"
        class="contact-card contact-map-card"
    >
        <div class="contact-map-wrap">
            <div class="contact-map-head">
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
            </div>

            <div class="contact-map-box">
                <iframe
                    id="contactMap"
                    class="contact-map-frame"
                    :src="content.mapSrc"
                    :title="content.mapTitle"
                    loading="lazy"
                    referrerpolicy="no-referrer-when-downgrade"
                ></iframe>

                <div
                    id="contactMapFallback"
                    class="contact-map-fallback"
                >
                    {{ content.fallbackText }}
                </div>

                <div
                    class="contact-map-brand-marker"
                    aria-hidden="true"
                >
                    <span class="contact-map-brand-pin">
                        <img
                            :src="heroLogoSrc"
                            alt=""
                        />
                    </span>
                </div>
            </div>

            <div class="contact-map-note">
                {{ t("contacts.navigationAddress") }}
                <strong>{{ content.address }}</strong>
            </div>
        </div>
    </div>
</template>
