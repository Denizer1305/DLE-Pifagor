<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";
import DashboardCalendarDayButton from "@/components/dashboard/calendar/DashboardCalendarDay.vue";
import DashboardCalendarLegend from "@/components/dashboard/calendar/DashboardCalendarLegend.vue";
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import { useCalendarPage } from "@/modules/calendar/composables/useCalendarPage";

const { logout } = useDashboardLogout();

const {
    content,
    displayedDays,
    errorMessage,
    form,
    isLoading,
    isSaving,
    model,
    monthLabel,
    saveError,
    selectedDateLabel,
    selectedDayItems,
    deletePlanItem,
    loadCalendar,
    selectDay,
    selectEventType,
    showNextMonth,
    showPreviousMonth,
    submitPlanItem,
} = useCalendarPage();
</script>

<template>
    <DashboardPageScaffold
        :model="model"
        :is-loading="false"
        error-message=""
        :loading-text="content.loadingText"
        @reload="loadCalendar"
        @logout="logout"
    >
        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="content.loadingText"
        />

        <DashboardStateView
            v-else-if="errorMessage"
            variant="error"
            :title="content.errorTitle"
            :text="errorMessage"
            :action-label="content.retryLabel"
            :action-icon="content.retryIcon"
            @action="loadCalendar"
        />

        <template v-else>
            <section class="calendar-page-hero fade-in visible">
                <div class="calendar-page-hero-copy">
                    <span class="dashboard-badge">
                        <i class="fas fa-calendar-days"></i>
                        {{ content.hero.badge }}
                    </span>

                    <h1>{{ content.hero.title }}</h1>
                    <p>{{ content.hero.text }}</p>
                </div>

                <div class="calendar-page-date-card">
                    <span>{{ content.calendar.selectedDayLabel }}</span>
                    <strong>{{ selectedDateLabel }}</strong>
                </div>
            </section>

            <section class="calendar-page-grid">
                <article class="calendar-page-card calendar-page-board">
                    <div class="calendar-page-board-head">
                        <button
                            type="button"
                            class="dashboard-calendar-nav"
                            :aria-label="content.calendar.previousMonthLabel"
                            @click="showPreviousMonth"
                        >
                            <i class="fas fa-chevron-left"></i>
                        </button>

                        <h2>{{ monthLabel }}</h2>

                        <button
                            type="button"
                            class="dashboard-calendar-nav"
                            :aria-label="content.calendar.nextMonthLabel"
                            @click="showNextMonth"
                        >
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>

                    <div class="calendar-page-legend-block">
                        <DashboardCalendarLegend :items="content.legend" />

                        <p class="calendar-page-legend-hint">
                            <i class="fas fa-circle-info"></i>
                            {{ content.legendHint }}
                        </p>
                    </div>

                    <div class="calendar-page-weekdays">
                        <span
                            v-for="weekday in content.calendar.weekdays"
                            :key="weekday"
                        >
                            {{ weekday }}
                        </span>
                    </div>

                    <div class="calendar-page-month">
                        <DashboardCalendarDayButton
                            v-for="day in displayedDays"
                            :key="day.date"
                            :day="day"
                            :is-active="day.isSelected"
                            @select="selectDay"
                        />
                    </div>
                </article>

                <aside class="calendar-page-side">
                    <form
                        class="calendar-page-card calendar-page-form"
                        @submit.prevent="submitPlanItem"
                    >
                        <div class="calendar-page-section-head">
                            <span class="dashboard-badge">
                                {{ content.calendar.createTitle }}
                            </span>
                        </div>

                        <label class="dashboard-create-field">
                            <span>{{ content.form.titleLabel }}</span>
                            <input
                                v-model="form.title"
                                type="text"
                                required
                                autocomplete="off"
                                :placeholder="content.form.titlePlaceholder"
                            />
                        </label>

                        <label class="dashboard-create-field">
                            <span>{{ content.form.dateLabel }}</span>
                            <input
                                v-model="form.date"
                                type="date"
                            />
                        </label>

                        <div class="dashboard-create-field">
                            <span>{{ content.form.eventTypeLabel }}</span>
                            <BaseSelect
                                id="calendar-page-event-type"
                                :model-value="form.eventType"
                                :options="content.eventTypeOptions"
                                :aria-label="content.form.eventTypeLabel"
                                @update:model-value="selectEventType"
                            />
                        </div>

                        <label class="dashboard-create-field">
                            <span>{{ content.form.textLabel }}</span>
                            <textarea
                                v-model="form.text"
                                rows="5"
                                :placeholder="content.form.textPlaceholder"
                            ></textarea>
                        </label>

                        <label class="dashboard-create-reminder">
                            <span class="dashboard-create-reminder__copy">
                                <strong>{{ content.form.notificationLabel }}</strong>
                                <span>{{ content.form.notificationText }}</span>
                            </span>

                            <input
                                v-model="form.notificationEnabled"
                                type="checkbox"
                            />
                            <span class="dashboard-create-reminder__toggle"></span>
                        </label>

                        <p
                            v-if="saveError"
                            class="contact-form-error calendar-page-error"
                        >
                            {{ saveError }}
                        </p>

                        <button
                            type="submit"
                            class="dashboard-create-modal__primary"
                            :disabled="isSaving"
                        >
                            <i class="fas fa-plus"></i>
                            {{ isSaving ? content.form.savingLabel : content.form.submitLabel }}
                        </button>
                    </form>

                    <article class="calendar-page-card calendar-page-plan">
                        <div class="calendar-page-section-head">
                            <span class="dashboard-badge">
                                <i class="fas fa-list-check"></i>
                                {{ content.calendar.eventsTitle }}
                            </span>
                            <strong>{{ selectedDateLabel }}</strong>
                        </div>

                        <div
                            v-if="selectedDayItems.length"
                            class="calendar-page-plan-list"
                        >
                            <div
                                v-for="item in selectedDayItems"
                                :key="item.id"
                                class="calendar-page-plan-item"
                                :class="`is-${item.event_type}`"
                            >
                                <div>
                                    <strong>{{ item.title }}</strong>
                                    <span>{{ item.text }}</span>
                                </div>

                                <button
                                    type="button"
                                    class="dashboard-panel-remove-icon"
                                    :aria-label="content.calendar.deleteLabel"
                                    @click="deletePlanItem(item.id)"
                                >
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>

                        <div
                            v-else
                            class="dashboard-empty-state"
                        >
                            <i class="fas fa-calendar-plus"></i>
                            <div>
                                <strong>{{ content.calendar.emptyDayTitle }}</strong>
                                <p>{{ content.calendar.emptyDayText }}</p>
                            </div>
                        </div>
                    </article>
                </aside>
            </section>
        </template>
    </DashboardPageScaffold>
</template>
