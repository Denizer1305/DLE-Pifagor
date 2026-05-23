<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import ContactFindCard from "@/modules/public/components/contacts/ContactFindCard.vue";
import ContactMapCard from "@/modules/public/components/contacts/ContactMapCard.vue";
import ContactSocialCard from "@/modules/public/components/contacts/ContactSocialCard.vue";
import type { ContactMainContent } from "@/modules/public/types/contact.types";

interface Props {
    content: ContactMainContent;
}

defineProps<Props>();
</script>

<template>
    <section
        id="contact-main"
        class="section contact-main"
    >
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="contact-shell fade-in visible">
                <div class="contact-layout">
                    <div class="contact-column">
                        <div class="contact-card">
                            <div class="contact-card-inner">
                                <div class="contact-card-topline">
                                    <i :class="content.info.toplineIcon"></i>
                                    {{ content.info.topline }}
                                </div>

                                <h3 class="contact-card-title">
                                    {{ content.info.title }}
                                </h3>

                                <p class="contact-card-text">
                                    {{ content.info.text }}
                                </p>

                                <div class="contact-info-list">
                                    <div
                                        v-for="item in content.info.items"
                                        :key="item.title"
                                        class="contact-info-item"
                                    >
                                        <div class="contact-info-icon">
                                            <i :class="item.icon"></i>
                                        </div>

                                        <div>
                                            <strong>{{ item.title }}</strong>

                                            <a
                                                v-if="item.href"
                                                :href="item.href"
                                            >
                                                {{ item.text }}
                                            </a>

                                            <span v-else>
                                                {{ item.text }}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <div class="contact-actions">
                                    <a
                                        v-for="action in content.info.actions"
                                        :key="action.label"
                                        :href="action.href"
                                        class="contact-action-chip"
                                    >
                                        <i :class="action.icon"></i>
                                        {{ action.label }}
                                    </a>
                                </div>
                            </div>
                        </div>

                        <div class="contact-card">
                            <div class="contact-card-inner">
                                <div class="contact-card-topline">
                                    <i :class="content.hours.toplineIcon"></i>
                                    {{ content.hours.topline }}
                                </div>

                                <h3 class="contact-card-title">
                                    {{ content.hours.title }}
                                </h3>

                                <p class="contact-card-text">
                                    {{ content.hours.text }}
                                </p>

                                <div class="contact-hours-grid">
                                    <div
                                        v-for="item in content.hours.items"
                                        :key="item.title"
                                        class="contact-hours-item"
                                    >
                                        <strong>{{ item.title }}</strong>
                                        <span>{{ item.text }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <ContactSocialCard :content="content.socials" />
                    </div>

                    <div class="contact-column">
                        <ContactMapCard :content="content.map" />

                        <ContactFindCard :content="content.find" />
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
