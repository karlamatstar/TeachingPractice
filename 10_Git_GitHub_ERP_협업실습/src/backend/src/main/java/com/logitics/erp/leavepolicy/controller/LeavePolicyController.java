package com.logitics.erp.leavepolicy.controller;

import com.logitics.erp.leavepolicy.dto.LeavePolicyRequest;
import com.logitics.erp.leavepolicy.dto.LeavePolicyResponse;
import com.logitics.erp.leavepolicy.service.LeavePolicyService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/leavePolicy")
public class LeavePolicyController {
	private final LeavePolicyService leavePolicyService;

	@GetMapping
	@Operation(summary = "직급별 휴가일수 조회")
	public List<LeavePolicyResponse> getLeavePolicies() {
		return leavePolicyService.getLeavePolicies();
	}

	@PostMapping
	@Operation(summary = "직급별 기준 휴가일수 추가")
	public Boolean addLeavePolicy(@RequestBody LeavePolicyRequest leavePolicyRequest) {
		return leavePolicyService.addLeavePolicy(leavePolicyRequest);
	}
}
