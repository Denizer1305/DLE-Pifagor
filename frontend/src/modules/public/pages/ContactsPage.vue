<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import PublicLayout from "@/layouts/PublicLayout.vue";
import ContactCtaSection from "@/modules/public/components/contacts/ContactCtaSection.vue";
import ContactFeedbackSection from "@/modules/public/components/contacts/ContactFeedbackSection.vue";
import ContactHeroSection from "@/modules/public/components/contacts/ContactHeroSection.vue";
import ContactInfoSection from "@/modules/public/components/contacts/ContactInfoSection.vue";
import { contactsPageContent } from "@/modules/public/data/contacts-page.data";

const { localizePublicContent } = useI18n();

const content = computed(() => {
    return localizePublicContent(contactsPageContent);
});
</script>

<template>
    <PublicLayout>
        <ContactHeroSection :content="content.hero" />

        <ContactInfoSection :content="content.main" />

        <ContactFeedbackSection :content="content.feedback" />

        <ContactCtaSection :content="content.cta" />
    </PublicLayout>
</template>
