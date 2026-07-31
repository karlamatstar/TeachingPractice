package com.logitics.erp.employeeappointment.entity;

public enum AppointmentType {

    NEW_HIRE("신규입사"),
    PROMOTION("승진"),
    DEMOTION("강등"),
    TRANSFER("전보"),
    POSITION_CHANGE("보직변경"),
    JOB_CHANGE("직무변경"),
    LEAVE("휴직"),
    REINSTATEMENT("복직"),
    DISPATCH("파견"),
    CONCURRENT_POSITION("겸직"),
    RETIREMENT("퇴직");

    private final String description;

    AppointmentType(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}