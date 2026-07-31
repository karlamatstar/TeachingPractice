package com.logitics.erp.leavetype.controller;

import com.logitics.erp.leavetype.dto.LeaveTypeResponse;
import com.logitics.erp.leavetype.service.LeaveTypeService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/leaveType")
public class LeaveTypeController {

	private final LeaveTypeService leaveTypeService;

	@GetMapping
	@Operation(summary = "특별휴가정책 조회")
	public List<LeaveTypeResponse> getLeaveType() {
		return leaveTypeService.getLeaveType();
	}
}
