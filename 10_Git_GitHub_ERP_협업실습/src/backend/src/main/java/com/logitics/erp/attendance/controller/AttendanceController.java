package com.logitics.erp.attendance.controller;

import com.logitics.erp.attendance.dto.*;
import com.logitics.erp.attendance.entity.Attendance;
import com.logitics.erp.attendance.service.AttendanceService;
import com.logitics.erp.employee.repository.EmployeeRepository;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/attendances")
public class AttendanceController {

	private final AttendanceService attendanceService;
	private final EmployeeRepository employeeRepository;

	@PostMapping("/checkin")
	@Operation(summary = "출근등록")
	public AttendResponse checkin(@RequestBody AttendRequest attendRequest, Authentication authentication) {
		String email = authentication.getName();
		String employeeNo = employeeRepository.findByEmail(email).orElseThrow(() -> new IllegalArgumentException("찾는 유저 정보가 없습니다.")).getEmployeeNo();
		attendRequest.setEmployeeNo(employeeNo);
		return attendanceService.attend(attendRequest);
	}

	@PostMapping("/checkout")
	@Operation(summary = "퇴근등록")
	public AttendResponse checkout(@RequestBody AttendRequest attendRequest, Authentication authentication) {
		String email = authentication.getName();
		String employeeNo = employeeRepository.findByEmail(email).orElseThrow(() -> new IllegalArgumentException("찾는 유저 정보가 없습니다.")).getEmployeeNo();
		attendRequest.setEmployeeNo(employeeNo);
		return attendanceService.checkout(attendRequest);
	}

	@GetMapping("/daily")
	@Operation(summary = "일일근태리스트조회")
	public List<AttendanceDailyResponse> getAttendanceDaily(@RequestParam(required = false) String findDate) {
		List<AttendanceDailyResponse> list = attendanceService.getAttendanceDaily(findDate);
		return list;
	}

	@GetMapping("/monthly")
	@Operation(summary = "월근태현황조회")
	public List<AttendanceResultResponse> getMonthly(@RequestParam(required = false) String findDate) {
		return attendanceService.getMonthly(findDate);
	}

	@GetMapping("/month")
	@Operation(summary = "월근태현황조회(미사용)")
	public List<AttendanceResultResponse> getMonthAttendance(
					@RequestParam(defaultValue = "10") int size,
					@RequestParam(defaultValue = "0") int page,
					@RequestParam(required = false) Long departmentId,
					@RequestParam(required = false) String startDate
	) {
		if (startDate.isEmpty()) {
			startDate = LocalDate.now().toString();
		}

		return attendanceService.getMonthAttendance(size, page, departmentId, startDate);
	}
}
