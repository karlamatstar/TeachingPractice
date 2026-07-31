package com.logitics.erp.employeeappointment.controller;


import com.logitics.erp.employeeappointment.dto.AppointmentHistoryRequest;
import com.logitics.erp.employeeappointment.dto.AppointmentHistoryResponse;
import com.logitics.erp.employeeappointment.dto.EmployeementAppointmentResponse;
import com.logitics.erp.employeeappointment.dto.RegisterAppointmentRequest;
import com.logitics.erp.employeeappointment.entity.AppointmentType;
import com.logitics.erp.employeeappointment.service.EmployeeAppointmentService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/appointment")
public class EmployeeAppointmentController {

	private final EmployeeAppointmentService employeeAppointmentService;

	@GetMapping
	public List<EmployeementAppointmentResponse> getEmployeeAppointmentHistory(
					@RequestParam(name = "page", defaultValue = "0") int page,
					@RequestParam(name = "size", defaultValue = "10") int size,
					@RequestParam(name = "keyword", required = false) String keyword
	) {
		return employeeAppointmentService.getEmployeeAppointmentHistory(page, size, keyword);
	}

	@PostMapping
	@Operation(summary = "발령등록", description = "발령을 등록합니다")
	public boolean registerAppointment(@RequestBody RegisterAppointmentRequest registerAppointmentRequest) {
		/**
		 * 승진발령, 전보발령(영업팁->물류팀), 보직발령, 휴직발령, 복직발령, 퇴직발령
		 */
		return employeeAppointmentService.registerAppointment(registerAppointmentRequest);
	}

    @GetMapping("/types")
    @Operation(summary = "발령구분전체조회", description = "발령구분 모든 타입 조회")
    public List<String> getAppointTypeList() {
        return employeeAppointmentService.getAppointTypeList();
    }

    @GetMapping("/history")
    @Operation(summary = "발령조회", description = "발령이력조회 합니다.")
    public List<AppointmentHistoryResponse> getAppointmentHistory(@RequestParam AppointmentHistoryRequest appointmentHistoryRequest) {
        return employeeAppointmentService.getAppointmentHistory(appointmentHistoryRequest);
    }



}
