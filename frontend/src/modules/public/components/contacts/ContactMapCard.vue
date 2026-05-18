<script setup>
import BaseIcon from "../../../../components/ui/BaseIcon.vue";
import { useContactMap } from "../composables/useContactMap";

defineProps({
    card: {
        type: Object,
        required: true,
    },
});

const {
    isMapLoading,
    isMapReady,
    isMapFailed,
} = useContactMap({
    mapElementId: "contactMap",
    coords: [56.11855, 40.37832],
    zoom: 16,
    balloonTitle: "Пифагор",
    balloonText: "г. Владимир",
    enabled: Boolean(import.meta.env.VITE_YANDEX_MAPS_API_KEY),
});
</script>

<template>
    <div
        :id="card.id"
        class="contact-card contact-map-card"
    >
        <div class="contact-map-wrap">
            <div class="contact-map-head">
                <div class="contact-card-topline">
                    <BaseIcon
                        :name="card.topline.icon"
                        size="15"
                    />

                    {{ card.topline.text }}
                </div>

                <h3 class="contact-card-title">
                    {{ card.title }}
                </h3>

                <p class="contact-card-text">
                    {{ card.text }}
                </p>
            </div>

            <div class="contact-map-box">
                <div
                    id="contactMap"
                    class="contact-map"
                    :class="{ 'contact-map--ready': isMapReady }"
                ></div>

                <a
                    v-if="isMapFailed"
                    :href="card.mapHref"
                    class="contact-map-placeholder"
                    target="_blank"
                    rel="noopener noreferrer"
                    :aria-label="`Открыть карту: ${card.address}`"
                >
                    <div class="contact-map-placeholder-icon">
                        <BaseIcon
                            name="map-marker"
                            size="30"
                        />
                    </div>

                    <strong>
                        Открыть адрес на Яндекс Картах
                    </strong>

                    <span>
                        {{ card.address }}
                    </span>
                </a>

                <div
                    v-else-if="isMapLoading"
                    class="contact-map-placeholder"
                >
                    <div class="contact-map-placeholder-icon">
                        <BaseIcon
                            name="spinner"
                            size="30"
                        />
                    </div>

                    <strong>
                        Загружаем карту
                    </strong>

                    <span>
                        {{ card.address }}
                    </span>
                </div>
            </div>

            <div class="contact-map-note">
                Адрес для навигации:
                <strong>{{ card.address }}</strong>
            </div>
        </div>
    </div>
</template>
