import type { ContactsPageContent } from "@/modules/public/types/contact.types";
import { contactFeedbackContent } from "@/modules/public/data/contacts-feedback.data";
import {
    contactCtaContent,
    contactHeroContent,
} from "@/modules/public/data/contacts-intro.data";
import { contactMainContent } from "@/modules/public/data/contacts-main.data";

export { contactFeedbackContent };

export const contactsPageContent: ContactsPageContent = {
    hero: contactHeroContent,
    main: contactMainContent,
    feedback: contactFeedbackContent,
    cta: contactCtaContent,
};
