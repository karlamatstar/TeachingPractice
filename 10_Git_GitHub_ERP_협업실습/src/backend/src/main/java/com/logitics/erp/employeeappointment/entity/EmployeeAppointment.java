package com.logitics.erp.employeeappointment.entity;

import com.logitics.erp.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Builder
public class EmployeeAppointment extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employeeAppointmentId;

    @Column(name = "appointment_type")
    @Enumerated(EnumType.STRING)
	private AppointmentType appointmentType;

	private LocalDate appointmentDate;
	private LocalDate effectiveDate;

	private Long fromDepartmentId;
	private Long toDepartmentId;

	private String fromPositionName;
	private String toPositionName;

	private String fromJobTitle;
	private String toJobTitle;

	private String reason;
	private String memo;


}
