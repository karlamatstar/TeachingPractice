package com.logitics.erp.attendance.dto;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class AttendanceDailyResponse {

    private String employeeNo;
    private String name;
    private String departmentName;
    private String positionName;

    private String checkInTime;
    private String checkOutTime;

    private String overTime;
    private String comment;

    private String attendanceStatusCode;

}
