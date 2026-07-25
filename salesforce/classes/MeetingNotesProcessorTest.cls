@IsTest
private class MeetingNotesProcessorTest {
    @IsTest
    static void normalizesSyntheticTranscript() {
        MeetingNotesProcessor.Request request = new MeetingNotesProcessor.Request();
        request.transcript = '  Decision: Use synthetic fixtures.  ';
        List<MeetingNotesProcessor.Response> results =
            MeetingNotesProcessor.process(new List<MeetingNotesProcessor.Request>{ request });
        System.assertEquals('Decision: Use synthetic fixtures.', results[0].normalizedTranscript);
    }
}

