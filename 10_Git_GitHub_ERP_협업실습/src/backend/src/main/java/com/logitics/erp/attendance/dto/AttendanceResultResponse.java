package com.logitics.erp.attendance.dto;

import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AttendanceResultResponse {
	private String name;
	private String departmentName;
	private List<String> days;
	private Map<String, Integer> summary;
}
