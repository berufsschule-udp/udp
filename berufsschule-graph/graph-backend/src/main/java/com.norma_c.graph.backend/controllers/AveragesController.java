package com.norma_c.graph.backend.controllers;

import com.norma_c.graph.backend.services.DatabaseService;
import jakarta.annotation.Nullable;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static com.norma_c.graph.backend.controllers.ControllersDescriptor.AVERAGES_URL;
import static com.norma_c.graph.backend.services.DatabaseService.injectSample;
import static java.util.Arrays.stream;
import static java.util.stream.Collectors.groupingBy;
import static org.springframework.http.ResponseEntity.badRequest;
import static org.springframework.http.ResponseEntity.ok;

@RestController
@RequiredArgsConstructor
public class AveragesController {
	private final DatabaseService databaseService;

	@GetMapping(AVERAGES_URL)
	public ResponseEntity<Map<String, List<Average>>> getAverages(
		@RequestParam("ids") String channelsId,
		@RequestParam("off") long offsetSeconds,
		@RequestParam("lim") long limitSeconds,
		@RequestParam("smp") @Nullable String sample
	) {
		return sample == null ? ok(getAveragesInternal(
			channelsId.split(","),
			offsetSeconds,
			limitSeconds
		)) : ok(getAveragesInternal(
			channelsId.split(","),
			offsetSeconds,
			limitSeconds,
			sample
		));
	}

	@ExceptionHandler(Exception.class)
	public ResponseEntity<String> handleException(Exception exception) {
		return badRequest().body(exception.getMessage());
	}

	private Map<String, List<Average>> getAveragesInternal(
		String[] channelsId,
		long offsetSeconds,
		long limitSeconds
	) {
		return databaseService.createNativeTypedQuery("""
				SELECT channel_id as channelId, value,
				DATEDIFF('s', timestamp, NOW()) as seconds
				FROM averages
				WHERE timestamp BETWEEN DATEADD('s', :from, NOW())
				AND DATEADD('s', :to, NOW())
				ORDER BY timestamp DESC""", Average.class)
			.setParameter("from", -offsetSeconds - limitSeconds)
			.setParameter("to", -offsetSeconds)
			.getResultStream()
			.filter(average -> stream(channelsId)
				.anyMatch(id -> id.equals(average.channelId())))
			.collect(groupingBy(Average::channelId));
	}

	private Map<String, List<Average>> getAveragesInternal(
		String[] channelsId,
		long offsetSeconds,
		long limitSeconds,
		String sample
	) throws IllegalArgumentException {
		return databaseService.createNativeTypedQuery("""
				SELECT channel_id as channelId, value,
				DATEDIFF('s', timestamp, NOW()) as seconds
				FROM (
					SELECT channel_id, AVG(value) as value, timestamp
					FROM averages
					WHERE timestamp BETWEEN DATEADD('s', :from, NOW())
						AND DATEADD('s', :to, NOW())
					SAMPLE BY %s FILL(NULL)
					ORDER BY timestamp DESC
				)""".formatted(injectSample(sample)), Average.class)
			.setParameter("from", -offsetSeconds - limitSeconds)
			.setParameter("to", -offsetSeconds)
			.getResultStream()
			.filter(average -> stream(channelsId)
				.anyMatch(id -> id.equals(average.channelId())))
			.collect(groupingBy(Average::channelId));
	}

	public record Average(
		String channelId,
		@Nullable Double value,
		long seconds
	) {}
}