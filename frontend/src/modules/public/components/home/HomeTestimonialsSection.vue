<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import HomeTestimonialCard from "@/modules/public/components/home/HomeTestimonialCard.vue";

interface Props {
    content: {
        label: string;
        title: string;
        description: string;
        items: {
            variant?: string;
            name: string;
            text: string;
            image: {
                src: string;
                alt: string;
            };
        }[];
    };
}

defineProps<Props>();
</script>

<template>
    <section
        id="testimonials"
        class="section testimonials-section"
    >
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="testimonials-shell fade-in">
                <div class="testimonials-mosaic">
                    <HomeTestimonialCard
                        v-for="testimonial in content.items"
                        :key="testimonial.name"
                        :testimonial="testimonial"
                    />
                </div>
            </div>
        </div>
    </section>
</template>
