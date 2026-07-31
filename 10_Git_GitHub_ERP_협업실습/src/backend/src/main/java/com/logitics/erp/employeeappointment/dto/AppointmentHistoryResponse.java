package com.logitics.erp.employeeappointment.dto;

import com.logitics.erp.employeeappointment.entity.AppointmentType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
public class AppointmentHistoryResponse {

    private Long employeeAppointmentId;

    private String employeeNo;
    private String name;
    private AppointmentType appointmentType;

    @Schema(description = "전부서")
    private String beforeDepartment;

    @Schema(description = "전직급")
    private String beforePositionName;

    @Schema(description = "후부서")
    private String afterDepartment;

    @Schema(description = "후직급")
    private String afterPositionName;

    @Schema(description = "발령일")
    private String appointedDate;

    @Schema(description = "등록자")
    private String registeredBy;

}
